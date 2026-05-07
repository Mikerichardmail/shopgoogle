import os
import re

file_path = r"f:\online shoping apps new\app\src\main\java\com\onlineshoppingapps\MainActivity.kt"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add imports if not exist
imports_to_add = [
    "import java.net.URL",
    "import java.net.HttpURLConnection",
    "import org.json.JSONArray",
    "import kotlin.concurrent.thread",
    "import android.util.Log"
]
for imp in imports_to_add:
    if imp not in content:
        content = content.replace("import android.os.Bundle", f"{imp}\nimport android.os.Bundle")

# Add variables
vars_to_add = """
    private var rvTopCoupons: RecyclerView? = null
    private var rvBestDeals: RecyclerView? = null
    private var couponAdapter: CouponAdapter? = null
"""
if "rvTopCoupons" not in content:
    content = content.replace("private var vpBanner: ViewPager2? = null", "private var vpBanner: ViewPager2? = null" + vars_to_add)

# Initialize views in initViews
init_views_add = """
        rvTopCoupons = findViewById(R.id.rvTopCoupons)
        rvBestDeals = findViewById(R.id.rvBestDeals)
"""
if "rvTopCoupons = findViewById" not in content:
    content = content.replace("vpBanner    = findViewById(R.id.vpBanner)", "vpBanner    = findViewById(R.id.vpBanner)\n" + init_views_add)

# Add method call in onCreate
if "fetchCouponsFromSupabase()" not in content:
    content = content.replace("setupSearch()", "setupSearch()\n        } catch (_: Throwable) {}\n        try {\n            setupCouponsList()\n            fetchCouponsFromSupabase()")

# Add the methods at the end (before last brace)
methods = """
    private fun setupCouponsList() {
        val rv = rvTopCoupons ?: return
        rv.layoutManager = androidx.recyclerview.widget.LinearLayoutManager(this)
        couponAdapter = CouponAdapter(emptyList())
        rv.adapter = couponAdapter
    }

    private fun fetchCouponsFromSupabase() {
        thread {
            try {
                val url = URL("https://fwhzasbjexillgfrvksx.supabase.co/rest/v1/coupons?status=eq.active")
                val conn = url.openConnection() as HttpURLConnection
                conn.requestMethod = "GET"
                conn.setRequestProperty("apikey", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4")
                conn.setRequestProperty("Authorization", "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3aHphc2JqZXhpbGxnZnJ2a3N4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY0Mzk5NzksImV4cCI6MjA5MjAxNTk3OX0.MfZPPcx4d7OkAo56emiRjF9FabceUweCVJqv48tXAv4")
                conn.setRequestProperty("Content-Type", "application/json")

                if (conn.responseCode == 200) {
                    val response = conn.inputStream.bufferedReader().use { it.readText() }
                    val jsonArray = JSONArray(response)
                    val newCoupons = mutableListOf<Coupon>()

                    for (i in 0 until jsonArray.length()) {
                        val obj = jsonArray.getJSONObject(i)
                        val storeId = obj.optString("store_id")
                        val store = allStores.find { it.id == storeId }
                        
                        newCoupons.add(
                            Coupon(
                                id = obj.optString("id"),
                                code = obj.optString("code"),
                                title = obj.optString("title"),
                                successScore = obj.optInt("success_score", 50),
                                storeName = store?.name ?: "Store",
                                storeIconRes = store?.iconRes ?: R.drawable.ic_launcher_foreground,
                                category = store?.categories?.firstOrNull() ?: "Shopping",
                                expiryDate = "Verified Today" // Mocked until added to DB
                            )
                        )
                    }

                    runOnUiThread {
                        couponAdapter?.updateData(newCoupons)
                    }
                } else {
                    Log.e("SUPABASE", "Error: ${conn.responseCode} ${conn.responseMessage}")
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
"""
if "fetchCouponsFromSupabase()" not in content[content.rfind("initViews"):]:
    content = content[:content.rfind("}")] + methods + "\n}\n"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated MainActivity.kt successfully.")
