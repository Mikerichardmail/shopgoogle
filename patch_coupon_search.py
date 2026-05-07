import os
import re

file_path = r"f:\online shoping apps new\app\src\main\java\com\onlineshoppingapps\MainActivity.kt"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add allCouponsList if not present
if "private var allCouponsList = listOf<Coupon>()" not in content:
    content = content.replace("private var couponAdapter: CouponAdapter? = null", 
                              "private var couponAdapter: CouponAdapter? = null\n    private var allCouponsList = listOf<Coupon>()")

# Add etSearchCoupons
if "private var etSearchCoupons: EditText? = null" not in content:
    content = content.replace("private var etSearch: EditText? = null", 
                              "private var etSearch: EditText? = null\n    private var etSearchCoupons: EditText? = null")

# Initialize etSearchCoupons
if "etSearchCoupons = findViewById(R.id.etSearchCoupons)" not in content:
    content = content.replace("rvAllCoupons = findViewById(R.id.rvAllCoupons)", 
                              "rvAllCoupons = findViewById(R.id.rvAllCoupons)\n        etSearchCoupons = findViewById(R.id.etSearchCoupons)")

# Update fetchCouponsFromSupabase
old_run_on_ui = """                    runOnUiThread {
                        couponAdapter?.updateData(newCoupons)
                    }"""
new_run_on_ui = """                    runOnUiThread {
                        allCouponsList = newCoupons
                        couponAdapter?.updateData(newCoupons)
                    }"""
if new_run_on_ui not in content:
    content = content.replace(old_run_on_ui, new_run_on_ui)

# Add search logic to setupCouponsList
search_logic = """
        etSearchCoupons?.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                val query = s?.toString()?.trim() ?: ""
                if (query.isEmpty()) {
                    couponAdapter?.updateData(allCouponsList)
                } else {
                    val filtered = allCouponsList.filter { 
                        it.storeName.contains(query, ignoreCase = true) || it.title.contains(query, ignoreCase = true)
                    }.sortedBy { it.storeName.lowercase() }
                    couponAdapter?.updateData(filtered)
                }
            }
            override fun afterTextChanged(s: Editable?) {}
        })
"""
if "etSearchCoupons?.addTextChangedListener" not in content:
    content = content.replace("rvAll.adapter = couponAdapter // Sharing the same adapter data\n        }", 
                              "rvAll.adapter = couponAdapter // Sharing the same adapter data\n        }\n" + search_logic)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Coupon search added.")
