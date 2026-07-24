package com.example.data

import kotlinx.coroutines.flow.Flow

class Repository(private val db: AppDatabase) {
    val allAccounts: Flow<List<UserAccount>> = db.userAccountDao().getAllAccountsFlow()
    val allProducts: Flow<List<Product>> = db.productDao().getAllProductsFlow()
    val allGroups: Flow<List<ProductGroup>> = db.productGroupDao().getAllGroupsFlow()
    val allUnits: Flow<List<ProductUnit>> = db.productUnitDao().getAllUnitsFlow()
    val allVouchers: Flow<List<Voucher>> = db.voucherDao().getAllVouchersFlow()
    val allVoucherItems: Flow<List<VoucherItem>> = db.voucherDao().getAllVoucherItemsFlow()
    val allCustomers: Flow<List<Customer>> = db.customerDao().getAllCustomersFlow()
    val allSuppliers: Flow<List<Supplier>> = db.supplierDao().getAllSuppliersFlow()
    val allPayments: Flow<List<Payment>> = db.paymentDao().getAllPaymentsFlow()
    val allExpenseCategories: Flow<List<ExpenseCategory>> = db.expenseCategoryDao().getAllCategoriesFlow()
    val allExpenses: Flow<List<Expense>> = db.expenseDao().getAllExpensesFlow()

    suspend fun getAccountByPhone(phone: String): UserAccount? {
        return db.userAccountDao().getAccountByPhone(phone)
    }

    suspend fun insertAccount(account: UserAccount) {
        db.userAccountDao().insertAccount(account)
    }

    suspend fun deleteAccount(account: UserAccount) {
        db.userAccountDao().deleteAccount(account)
    }

    suspend fun insertProduct(product: Product): Long {
        return db.productDao().insertProduct(product)
    }

    suspend fun updateProduct(product: Product) {
        db.productDao().updateProduct(product)
    }

    suspend fun deleteProduct(product: Product) {
        db.productDao().deleteProduct(product)
    }

    suspend fun updateStock(productId: Long, quantity: Int) {
        db.productDao().updateStock(productId, quantity)
    }

    suspend fun getProductDirect(id: Long): Product? {
        return db.productDao().getProductById(id)
    }

    suspend fun insertGroup(group: ProductGroup) {
        db.productGroupDao().insertGroup(group)
    }

    suspend fun deleteGroup(group: ProductGroup) {
        db.productGroupDao().deleteGroup(group)
    }

    suspend fun insertUnit(unit: ProductUnit) {
        db.productUnitDao().insertUnit(unit)
    }

    suspend fun deleteUnit(unit: ProductUnit) {
        db.productUnitDao().deleteUnit(unit)
    }

    suspend fun insertVoucher(voucher: Voucher) {
        db.voucherDao().insertVoucher(voucher)
    }

    suspend fun insertVoucherItem(item: VoucherItem) {
        db.voucherDao().insertVoucherItem(item)
    }

    fun getVoucherItems(voucherId: String): Flow<List<VoucherItem>> {
        return db.voucherDao().getVoucherItemsFlow(voucherId)
    }

    suspend fun getVoucherItemsDirect(voucherId: String): List<VoucherItem> {
        return db.voucherDao().getVoucherItemsDirect(voucherId)
    }

    suspend fun deleteVoucherItems(voucherId: String) {
        db.voucherDao().deleteVoucherItems(voucherId)
    }

    suspend fun deleteVoucher(voucherId: String) {
        db.voucherDao().deleteVoucher(voucherId)
    }

    suspend fun getVoucherDirect(voucherId: String): Voucher? {
        return db.voucherDao().getVoucherDirect(voucherId)
    }

    suspend fun insertCustomer(customer: Customer) {
        db.customerDao().insertCustomer(customer)
    }

    suspend fun updateCustomer(customer: Customer) {
        db.customerDao().updateCustomer(customer)
    }

    suspend fun deleteCustomer(customer: Customer) {
        db.customerDao().deleteCustomer(customer)
    }

    suspend fun insertSupplier(supplier: Supplier) {
        db.supplierDao().insertSupplier(supplier)
    }

    suspend fun updateSupplier(supplier: Supplier) {
        db.supplierDao().updateSupplier(supplier)
    }

    suspend fun deleteSupplier(supplier: Supplier) {
        db.supplierDao().deleteSupplier(supplier)
    }

    suspend fun insertPayment(payment: Payment) {
        db.paymentDao().insertPayment(payment)
    }

    suspend fun updatePayment(payment: Payment) {
        db.paymentDao().updatePayment(payment)
    }

    suspend fun deletePayment(payment: Payment) {
        db.paymentDao().deletePayment(payment)
    }

    suspend fun insertExpenseCategory(category: ExpenseCategory): Long {
        return db.expenseCategoryDao().insertCategory(category)
    }

    suspend fun deleteExpenseCategory(category: ExpenseCategory) {
        db.expenseCategoryDao().deleteCategory(category)
    }

    suspend fun getExpenseById(id: Long): Expense? {
        return db.expenseDao().getExpenseById(id)
    }

    suspend fun insertExpense(expense: Expense): Long {
        return db.expenseDao().insertExpense(expense)
    }

    suspend fun updateExpense(expense: Expense) {
        db.expenseDao().updateExpense(expense)
    }

    suspend fun deleteExpense(expense: Expense) {
        db.expenseDao().deleteExpense(expense)
    }
}
