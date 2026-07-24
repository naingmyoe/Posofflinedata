/**
 * Cloudflare Worker Backend for UN POS Application
 * Database: Cloudflare D1 (env.DB)
 *
 * Setup Instructions:
 * 1. Install wrangler: npm install -g wrangler
 * 2. Login to Cloudflare: wrangler login
 * 3. Create D1 Database: wrangler d1 create pos_db
 * 4. Add D1 binding to wrangler.toml:
 *    [[d1_databases]]
 *    binding = "DB"
 *    database_name = "pos_db"
 *    database_id = "<your-d1-database-id>"
 * 5. Deploy Worker: wrangler deploy
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Standard CORS Headers for Android / Web access
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Content-Type': 'application/json'
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // Initialize D1 table if not exists
      if (env.DB) {
        await env.DB.prepare(`
          CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_no TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            business_name TEXT NOT NULL,
            business_type TEXT NOT NULL,
            address TEXT,
            role TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            device_id TEXT,
            status TEXT DEFAULT 'off',
            created_at INTEGER NOT NULL
          )
        `).run();

        // Safely add missing columns for existing tables
        try { await env.DB.prepare("ALTER TABLE users ADD COLUMN device_id TEXT").run(); } catch (e) {}
        try { await env.DB.prepare("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'off'").run(); } catch (e) {}
      }

      // API: REGISTER USER (POST /api/register)
      if (path === '/api/register' && request.method === 'POST') {
        const body = await request.json();
        const { phoneNo, username, businessName, businessType, address, role, password, deviceId } = body;

        if (!phoneNo || !username || !password) {
          return new Response(
            JSON.stringify({ success: false, message: 'လိုအပ်သော အချက်အလက်များ မပြည့်စုံပါ (Missing required fields)' }),
            { status: 400, headers: corsHeaders }
          );
        }

        if (env.DB) {
          // Check if phone number already exists in Cloudflare D1
          const existing = await env.DB.prepare('SELECT id, device_id FROM users WHERE phone_no = ?').bind(phoneNo).first();
          if (existing) {
            // Update device_id if missing or re-registering
            await env.DB.prepare('UPDATE users SET device_id = ?, username = ?, password_hash = ? WHERE phone_no = ?')
              .bind(deviceId || '', username, password, phoneNo)
              .run();

            return new Response(
              JSON.stringify({
                success: true,
                message: 'အကောင့် ပြန်လည်ပြင်ဆင်ပြီးပါပြီ (User updated, pending activation)',
                status: 'off',
                user: { phoneNo, username, businessName, businessType, address, role, deviceId, status: 'off' }
              }),
              { status: 200, headers: corsHeaders }
            );
          }

          // Insert into D1 with default status = 'off'
          const now = Date.now();
          await env.DB.prepare(`
            INSERT INTO users (phone_no, username, business_name, business_type, address, role, password_hash, device_id, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'off', ?)
          `).bind(phoneNo, username, businessName || '', businessType || '', address || '', role || 'ADMIN', password, deviceId || '', now).run();
        }

        return new Response(
          JSON.stringify({
            success: true,
            message: 'အကောင့် အောင်မြင်စွာ ပြုလုပ်ပြီးပါပြီ (Registration successful, pending activation)',
            status: 'off',
            user: { phoneNo, username, businessName, businessType, address, role, deviceId, status: 'off' }
          }),
          { status: 200, headers: corsHeaders }
        );
      }

      // API: LOGIN USER (POST /api/login)
      if (path === '/api/login' && request.method === 'POST') {
        const body = await request.json();
        const { phoneNo, password, deviceId } = body;

        if (!phoneNo || !password) {
          return new Response(
            JSON.stringify({ success: false, message: 'ဖုန်းနံပါတ် နှင့် Password ဖြည့်ပါ (Missing login credentials)' }),
            { status: 400, headers: corsHeaders }
          );
        }

        if (env.DB) {
          const user = await env.DB.prepare('SELECT * FROM users WHERE phone_no = ? AND password_hash = ?')
            .bind(phoneNo, password)
            .first();

          if (!user) {
            return new Response(
              JSON.stringify({ success: false, message: 'ဖုန်းနံပါတ် သို့မဟုတ် Password မှားယွင်းနေပါသည် (Invalid credentials)' }),
              { status: 401, headers: corsHeaders }
            );
          }

          // Verify deviceId matching
          if (deviceId && user.device_id && user.device_id !== '' && user.device_id !== deviceId) {
            return new Response(
              JSON.stringify({
                success: false,
                message: 'Device ID မကိုက်ညီပါ။ သင်မှတ်ပုံတင်ထားသော စက်မဟုတ်ပါ (Device ID mismatch)'
              }),
              { status: 400, headers: corsHeaders }
            );
          }

          // Update device_id if it was not stored previously
          if (deviceId && (!user.device_id || user.device_id === '')) {
            await env.DB.prepare('UPDATE users SET device_id = ? WHERE phone_no = ?').bind(deviceId, phoneNo).run();
          }

          const userStatus = user.status || 'off';
          if (userStatus !== 'on') {
            return new Response(
              JSON.stringify({
                success: false,
                status: 'off',
                message: 'အကောင့်ဖွင့်ရန် စောင့်ဆိုင်းနေဆဲဖြစ်ပါသည် (Account is pending activation)',
                user: {
                  phoneNo: user.phone_no,
                  username: user.username,
                  deviceId: user.device_id || deviceId,
                  status: 'off'
                }
              }),
              { status: 403, headers: corsHeaders }
            );
          }

          return new Response(
            JSON.stringify({
              success: true,
              status: 'on',
              message: 'Login successful',
              user: {
                phoneNo: user.phone_no,
                username: user.username,
                businessName: user.business_name,
                businessType: user.business_type,
                address: user.address,
                role: user.role,
                deviceId: user.device_id || deviceId,
                status: 'on'
              }
            }),
            { status: 200, headers: corsHeaders }
          );
        }

        return new Response(
          JSON.stringify({ success: true, status: 'on', message: 'Mock Login Successful' }),
          { status: 200, headers: corsHeaders }
        );
      }

      // API: CHECK STATUS (GET or POST /api/check-status)
      if (path === '/api/check-status') {
        let phoneNo = url.searchParams.get('phoneNo');
        let deviceId = url.searchParams.get('deviceId');

        if (request.method === 'POST') {
          try {
            const body = await request.json();
            if (body.phoneNo) phoneNo = body.phoneNo;
            if (body.deviceId) deviceId = body.deviceId;
          } catch (e) {}
        }

        if (env.DB) {
          let user = null;
          if (phoneNo) {
            user = await env.DB.prepare('SELECT phone_no, username, device_id, status FROM users WHERE phone_no = ?').bind(phoneNo).first();
          } else if (deviceId) {
            user = await env.DB.prepare('SELECT phone_no, username, device_id, status FROM users WHERE device_id = ?').bind(deviceId).first();
          }

          if (user) {
            return new Response(
              JSON.stringify({
                success: true,
                status: user.status || 'off',
                phoneNo: user.phone_no,
                username: user.username,
                deviceId: user.device_id
              }),
              { status: 200, headers: corsHeaders }
            );
          } else {
            return new Response(
              JSON.stringify({ success: false, status: 'off', message: 'User not found' }),
              { status: 404, headers: corsHeaders }
            );
          }
        }

        return new Response(
          JSON.stringify({ success: true, status: 'off', message: 'User status checked' }),
          { status: 200, headers: corsHeaders }
        );
      }

      // API: ADMIN TOGGLE STATUS (POST /api/toggle-status)
      if (path === '/api/toggle-status' && request.method === 'POST') {
        const body = await request.json();
        const { phoneNo, status } = body; // status = 'on' or 'off'

        if (!phoneNo || !status) {
          return new Response(
            JSON.stringify({ success: false, message: 'Missing phoneNo or status' }),
            { status: 400, headers: corsHeaders }
          );
        }

        if (env.DB) {
          await env.DB.prepare('UPDATE users SET status = ? WHERE phone_no = ?').bind(status, phoneNo).run();
          return new Response(
            JSON.stringify({ success: true, message: `Status updated to ${status} for ${phoneNo}`, phoneNo, status }),
            { status: 200, headers: corsHeaders }
          );
        }

        return new Response(
          JSON.stringify({ success: true, message: `Mock status updated to ${status}` }),
          { status: 200, headers: corsHeaders }
        );
      }

      // API: GET ALL USERS (GET /api/users)
      if (path === '/api/users' && request.method === 'GET') {
        if (env.DB) {
          const { results } = await env.DB.prepare('SELECT phone_no, username, business_name, business_type, address, role, device_id, status, created_at FROM users').all();
          return new Response(JSON.stringify({ success: true, users: results }), { status: 200, headers: corsHeaders });
        }
        return new Response(JSON.stringify({ success: true, users: [] }), { status: 200, headers: corsHeaders });
      }

      return new Response(
        JSON.stringify({ success: false, message: 'Endpoint not found' }),
        { status: 404, headers: corsHeaders }
      );
    } catch (err) {
      return new Response(
        JSON.stringify({ success: false, message: err.message }),
        { status: 500, headers: corsHeaders }
      );
    }
  }
};
