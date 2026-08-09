package com.example.data

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface UserAccountDao {
    @Query("SELECT * FROM user_accounts")
    fun getAllAccountsFlow(): Flow<List<UserAccount>>

    @Query("SELECT * FROM user_accounts WHERE phoneNo = :phone LIMIT 1")
    suspend fun getAccountByPhone(phone: String): UserAccount?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAccount(account: UserAccount)

    @Delete
    suspend fun deleteAccount(account: UserAccount)
}

@Dao
interface ProductDao {
    @Query("SELECT * FROM products ORDER BY id DESC")
    fun getAllProductsFlow(): Flow<List<Product>>

    @Query("SELECT * FROM products WHERE id = :id LIMIT 1")
    suspend fun getProductById(id: Long): Product?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertProduct(product: Product): Long

    @Update
    suspend fun updateProduct(product: Product)

    @Delete
    suspend fun deleteProduct(product: Product)

    @Query("UPDATE products SET quantity = :qty WHERE id = :id")
    suspend fun updateStock(id: Long, qty: Int)

    @Query("UPDATE products SET quantity = :qty, alertQuantity = :alertQty WHERE id = :id")
    suspend fun updateStockAndAlert(id: Long, qty: Int, alertQty: Int)
}

@Dao
interface ProductGroupDao {
    @Query("SELECT * FROM product_groups ORDER BY name ASC")
    fun getAllGroupsFlow(): Flow<List<ProductGroup>>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertGroup(group: ProductGroup)

    @Delete
    suspend fun deleteGroup(group: ProductGroup)
}

@Dao
interface ProductUnitDao {
    @Query("SELECT * FROM product_units ORDER BY name ASC")
    fun getAllUnitsFlow(): Flow<List<ProductUnit>>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertUnit(unit: ProductUnit)

    @Delete
    suspend fun deleteUnit(unit: ProductUnit)
}

@Dao
interface VoucherDao {
    @Query("SELECT * FROM vouchers ORDER BY timestamp DESC")
    fun getAllVouchersFlow(): Flow<List<Voucher>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertVoucher(voucher: Voucher)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertVoucherItem(item: VoucherItem)

    @Query("SELECT * FROM voucher_items WHERE voucherId = :voucherId")
    fun getVoucherItemsFlow(voucherId: String): Flow<List<VoucherItem>>

    @Query("SELECT * FROM voucher_items")
    fun getAllVoucherItemsFlow(): Flow<List<VoucherItem>>

    @Query("SELECT * FROM voucher_items WHERE voucherId = :voucherId")
    suspend fun getVoucherItemsDirect(voucherId: String): List<VoucherItem>

    @Query("DELETE FROM voucher_items WHERE voucherId = :voucherId")
    suspend fun deleteVoucherItems(voucherId: String)

    @Query("SELECT * FROM vouchers WHERE receiptNo = :voucherId")
    suspend fun getVoucherDirect(voucherId: String): Voucher?

    @Query("DELETE FROM vouchers WHERE receiptNo = :voucherId")
    suspend fun deleteVoucher(voucherId: String)
}

@Dao
interface CustomerDao {
    @Query("SELECT * FROM customers ORDER BY name ASC")
    fun getAllCustomersFlow(): Flow<List<Customer>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertCustomer(customer: Customer)

    @Update
    suspend fun updateCustomer(customer: Customer)

    @Delete
    suspend fun deleteCustomer(customer: Customer)
}

@Dao
interface SupplierDao {
    @Query("SELECT * FROM suppliers ORDER BY name ASC")
    fun getAllSuppliersFlow(): Flow<List<Supplier>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSupplier(supplier: Supplier)

    @Update
    suspend fun updateSupplier(supplier: Supplier)

    @Delete
    suspend fun deleteSupplier(supplier: Supplier)
}

@Dao
interface PaymentDao {
    @Query("SELECT * FROM payments ORDER BY id DESC")
    fun getAllPaymentsFlow(): Flow<List<Payment>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPayment(payment: Payment)

    @Update
    suspend fun updatePayment(payment: Payment)

    @Delete
    suspend fun deletePayment(payment: Payment)
}

@Dao
interface ExpenseCategoryDao {
    @Query("SELECT * FROM expense_categories ORDER BY name ASC")
    fun getAllCategoriesFlow(): Flow<List<ExpenseCategory>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertCategory(category: ExpenseCategory): Long

    @Delete
    suspend fun deleteCategory(category: ExpenseCategory)
}

@Dao
interface ExpenseDao {
    @Query("SELECT * FROM expenses ORDER BY timestamp DESC")
    fun getAllExpensesFlow(): Flow<List<Expense>>

    @Query("SELECT * FROM expenses WHERE id = :id LIMIT 1")
    suspend fun getExpenseById(id: Long): Expense?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertExpense(expense: Expense): Long

    @Update
    suspend fun updateExpense(expense: Expense)

    @Delete
    suspend fun deleteExpense(expense: Expense)
}
