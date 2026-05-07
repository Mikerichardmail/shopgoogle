import os

file_path = r"f:\online shoping apps new\app\src\main\java\com\onlineshoppingapps\MainActivity.kt"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add view variables
vars_to_add = """
    private var rvAllStores: RecyclerView? = null
    private var rvAllCoupons: RecyclerView? = null
"""
if "rvAllStores" not in content:
    content = content.replace("private var rvBestDeals: RecyclerView? = null", "private var rvBestDeals: RecyclerView? = null" + vars_to_add)

# Initialize container views
init_views_add = """
        rvAllStores = findViewById(R.id.rvAllStores)
        rvAllCoupons = findViewById(R.id.rvAllCoupons)
        findViewById<View>(R.id.btnShareApp)?.setOnClickListener { shareApp() }
"""
if "rvAllStores = findViewById" not in content:
    content = content.replace("rvBestDeals = findViewById(R.id.rvBestDeals)", "rvBestDeals = findViewById(R.id.rvBestDeals)\n" + init_views_add)

# In setupStores, add initialization for rvAllStores
setup_stores_add = """
        // Also populate the All Stores tab
        rvAllStores?.layoutManager = GridLayoutManager(this, 4)
        rvAllStores?.adapter = StoreAdapter(allStores, { openLink(it.link) }, { store, pos -> 
            store.isFavorite = !store.isFavorite
            rvAllStores?.adapter?.notifyItemChanged(pos)
        })
"""
if "rvAllStores?.layoutManager" not in content:
    # find where storeAdapter is created
    content = content.replace("storeAdapter = StoreAdapter(allStores", setup_stores_add + "\n        storeAdapter = StoreAdapter(allStores")

# In setupCouponsList, add initialization for rvAllCoupons
setup_coupons_add = """
        val rvAll = rvAllCoupons
        if (rvAll != null) {
            rvAll.layoutManager = androidx.recyclerview.widget.LinearLayoutManager(this)
            rvAll.adapter = couponAdapter // Sharing the same adapter data
        }
"""
if "rvAllCoupons" not in content[content.find("private fun setupCouponsList"):content.find("private fun fetchCouponsFromSupabase")]:
    content = content.replace("rv.adapter = couponAdapter", "rv.adapter = couponAdapter\n" + setup_coupons_add)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("MainActivity.kt patched with tab content logic.")
