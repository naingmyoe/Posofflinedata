import re

file_path = 'app/src/main/java/com/example/ui/screens/POSScreens.kt'
with open(file_path, 'r') as f:
    content = f.read()

# 1. SASLogo replacement
old_logo = '''@Composable
fun SASLogo(modifier: Modifier = Modifier, size: Dp = 80.dp) {
    Box(
        modifier = modifier
            .size(size)
            .background(BrandPurple, shape = RoundedCornerShape(percent = 25)),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = "S",
            color = Color.White,
            fontSize = (size.value * 0.55f).sp,
            fontWeight = FontWeight.Bold
        )
    }
}'''

new_logo = '''@Composable
fun UNLogo(modifier: Modifier = Modifier, size: Dp = 80.dp) {
    Box(
        modifier = modifier
            .size(size)
            .background(BrandPurple, shape = RoundedCornerShape(percent = 28)),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = "UN",
            color = Color.White,
            fontSize = (size.value * 0.45f).sp,
            fontWeight = FontWeight.Bold
        )
    }
}

@Composable
fun SASLogo(modifier: Modifier = Modifier, size: Dp = 80.dp) {
    UNLogo(modifier = modifier, size = size)
}'''

# 2. Drawer replacement
old_drawer = '''    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet {
                Column(
                    modifier = Modifier
                        .fillMaxHeight()
                        .width(300.dp)
                        .background(Color.White)
                ) {
                    // Drawer Header with SAS POS style
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(BrandPurple)
                            .padding(24.dp)
                    ) {
                        Column {
                            SASLogo(size = 50.dp, modifier = Modifier.padding(bottom = 12.dp))
                            Text(
                                text = "SAS MOBILE POS",
                                color = Color.White,
                                fontWeight = FontWeight.Bold,
                                fontSize = 18.sp
                            )
                            Text(
                                text = "Version 1.2.5",
                                color = Color.LightGray,
                                fontSize = 13.sp
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))

                    // Menu Items
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Filled.Home, "Home") },
                        label = { Text("Home") },
                        selected = true,
                        onClick = {
                            scope.launch { drawerState.close() }
                        },
                        modifier = Modifier.padding(horizontal = 12.dp)
                    )

                    NavigationDrawerItem(
                        icon = { Icon(Icons.Filled.People, "Accounts") },
                        label = { Text("Accounts") },
                        selected = false,
                        onClick = {
                            scope.launch {
                                drawerState.close()
                                navController.navigate("accounts_list")
                            }
                        },
                        modifier = Modifier.padding(horizontal = 12.dp)
                    )

                    NavigationDrawerItem(
                        icon = { Icon(Icons.Filled.Settings, "Setting") },
                        label = { Text("Setting") },
                        selected = false,
                        onClick = {
                            scope.launch {
                                drawerState.close()
                                navController.navigate("settings")
                            }
                        },
                        modifier = Modifier.padding(horizontal = 12.dp)
                    )

                    NavigationDrawerItem(
                        icon = { Icon(Icons.Filled.Info, "About") },
                        label = { Text("About") },
                        selected = false,
                        onClick = {
                            scope.launch {
                                drawerState.close()
                                navController.navigate("about")
                            }
                        },
                        modifier = Modifier.padding(horizontal = 12.dp)
                    )

                    Spacer(modifier = Modifier.weight(1f))

                    // Log Out
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Filled.ExitToApp, "Logout", tint = Color.Red) },
                        label = { Text("Logout", color = Color.Red) },
                        selected = false,
                        onClick = {
                            scope.launch {
                                drawerState.close()
                                viewModel.logout()
                                navController.navigate("login") {
                                    popUpTo("dashboard") { inclusive = true }
                                }
                            }
                        },
                        modifier = Modifier.padding(12.dp)
                    )
                }
            }
        }
    )'''

new_drawer = '''    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet(
                drawerContainerColor = AppCardBg
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxHeight()
                        .width(300.dp)
                        .background(AppCardBg)
                ) {
                    // Drawer Header with UN POS style
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(AppCardBg)
                            .padding(top = 32.dp, bottom = 16.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            UNLogo(size = 72.dp, modifier = Modifier.padding(bottom = 12.dp))
                            Text(
                                text = "UN MOBILE POS",
                                color = AppTextColor,
                                fontWeight = FontWeight.Bold,
                                fontSize = 18.sp
                            )
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                text = "Version 1.2.5",
                                color = AppSubTextColor,
                                fontSize = 13.sp
                            )
                        }
                    }

                    HorizontalDivider(
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                        color = Color.LightGray.copy(alpha = 0.3f)
                    )

                    val itemColors = NavigationDrawerItemDefaults.colors(
                        selectedContainerColor = if (globalIsDarkTheme) Color(0xFF322A4E) else Color(0xFFEDE7F6),
                        selectedIconColor = BrandPurple,
                        selectedTextColor = BrandPurple,
                        unselectedIconColor = AppTextColor,
                        unselectedTextColor = AppTextColor
                    )

                    // Menu Items
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Filled.Home, "Home") },
                        label = { Text("Home", fontWeight = FontWeight.SemiBold) },
                        selected = true,
                        colors = itemColors,
                        onClick = {
                            scope.launch { drawerState.close() }
                        },
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp)
                    )

                    NavigationDrawerItem(
                        icon = { Icon(Icons.Filled.People, "Accounts") },
                        label = { Text("Accounts") },
                        selected = false,
                        colors = itemColors,
                        onClick = {
                            scope.launch {
                                drawerState.close()
                                navController.navigate("accounts_list")
                            }
                        },
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp)
                    )

                    NavigationDrawerItem(
                        icon = { Icon(Icons.Filled.Settings, "Setting") },
                        label = { Text("Setting") },
                        selected = false,
                        colors = itemColors,
                        onClick = {
                            scope.launch {
                                drawerState.close()
                                navController.navigate("settings")
                            }
                        },
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp)
                    )

                    NavigationDrawerItem(
                        icon = { Icon(Icons.Filled.Info, "About") },
                        label = { Text("About") },
                        selected = false,
                        colors = itemColors,
                        onClick = {
                            scope.launch {
                                drawerState.close()
                                navController.navigate("about")
                            }
                        },
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 2.dp)
                    )

                    Spacer(modifier = Modifier.weight(1f))

                    // Log Out
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Filled.ExitToApp, "Logout", tint = Color.Red) },
                        label = { Text("Logout", color = Color.Red) },
                        selected = false,
                        colors = itemColors,
                        onClick = {
                            scope.launch {
                                drawerState.close()
                                viewModel.logout()
                                navController.navigate("login") {
                                    popUpTo("dashboard") { inclusive = true }
                                }
                            }
                        },
                        modifier = Modifier.padding(12.dp)
                    )
                }
            }
        }
    )'''

# 3. TopAppBar & Scaffold background
old_topbar = '''                    colors = TopAppBarDefaults.centerAlignedTopAppBarColors(containerColor = Color.White)
                )
            }
        ) { innerPadding ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .background(LightBg)'''

new_topbar = '''                    colors = TopAppBarDefaults.centerAlignedTopAppBarColors(containerColor = AppCardBg)
                )
            }
        ) { innerPadding ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .background(AppBgColor)'''

# 4. DashboardSection dark theme colors
old_dash = '''        Card(
            colors = CardDefaults.cardColors(containerColor = Color.White),
            shape = RoundedCornerShape(16.dp),
            border = BorderStroke(1.dp, Color(0xFFE2DDF0)),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(8.dp)) {
                items.chunked(columns).forEach { rowItems ->
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        rowItems.forEach { item ->
                            Column(
                                horizontalAlignment = Alignment.CenterHorizontally,
                                modifier = Modifier
                                    .weight(1f)
                                    .clickable {
                                        if (item.route != null) {
                                            navController.navigate(item.route)
                                        } else {
                                            item.action?.invoke()
                                        }
                                    }
                                    .padding(vertical = 12.dp, horizontal = 4.dp)
                            ) {
                                Box(
                                    modifier = Modifier
                                        .size(44.dp)
                                        .background(Color(0xFFECE9F6), shape = RoundedCornerShape(12.dp)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(
                                        imageVector = item.icon,
                                        contentDescription = item.title,
                                        tint = BrandPurple,
                                        modifier = Modifier.size(24.dp)
                                    )
                                }
                                Spacer(modifier = Modifier.height(8.dp))
                                Text(
                                    text = item.title,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Medium,
                                    color = Color.Black,'''

new_dash = '''        Card(
            colors = CardDefaults.cardColors(containerColor = AppCardBg),
            shape = RoundedCornerShape(16.dp),
            border = BorderStroke(1.dp, if (globalIsDarkTheme) Color(0xFF2C2B35) else Color(0xFFE2DDF0)),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(8.dp)) {
                items.chunked(columns).forEach { rowItems ->
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        rowItems.forEach { item ->
                            Column(
                                horizontalAlignment = Alignment.CenterHorizontally,
                                modifier = Modifier
                                    .weight(1f)
                                    .clickable {
                                        if (item.route != null) {
                                            navController.navigate(item.route)
                                        } else {
                                            item.action?.invoke()
                                        }
                                    }
                                    .padding(vertical = 12.dp, horizontal = 4.dp)
                            ) {
                                Box(
                                    modifier = Modifier
                                        .size(44.dp)
                                        .background(AppHeaderBg, shape = RoundedCornerShape(12.dp)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(
                                        imageVector = item.icon,
                                        contentDescription = item.title,
                                        tint = BrandPurple,
                                        modifier = Modifier.size(24.dp)
                                    )
                                }
                                Spacer(modifier = Modifier.height(8.dp))
                                Text(
                                    text = item.title,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Medium,
                                    color = AppTextColor,'''

# 5. Receipt Unit replacement
old_receipt_qty = 'val qty = "${item.quantity} pcs"'
new_receipt_qty = '''val unitStr = item.product.unit.ifBlank { "pcs" }
        val qty = "${item.quantity} $unitStr"'''

print("Match status:")
print("logo:", old_logo in content)
print("drawer:", old_drawer in content)
print("topbar:", old_topbar in content)
print("dash:", old_dash in content)
print("receipt_qty:", old_receipt_qty in content)

new_content = content.replace(old_logo, new_logo).replace(old_drawer, new_drawer).replace(old_topbar, new_topbar).replace(old_dash, new_dash).replace(old_receipt_qty, new_receipt_qty)

with open(file_path, 'w') as f:
    f.write(new_content)

print('Update script executed successfully!')
