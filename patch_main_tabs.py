import os

file_path = r"f:\online shoping apps new\app\src\main\java\com\onlineshoppingapps\MainActivity.kt"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add view variables
vars_to_add = """
    private var containerHome: View? = null
    private var containerCategories: View? = null
    private var containerCoupons: View? = null
    private var containerStores: View? = null
    private var containerProfile: View? = null
"""
if "containerHome" not in content:
    content = content.replace("private var vpBanner: ViewPager2? = null", "private var vpBanner: ViewPager2? = null" + vars_to_add)

# Initialize container views
init_views_add = """
        containerHome = findViewById(R.id.containerHome)
        containerCategories = findViewById(R.id.containerCategories)
        containerCoupons = findViewById(R.id.containerCoupons)
        containerStores = findViewById(R.id.containerStores)
        containerProfile = findViewById(R.id.containerProfile)
        
        val bottomNavigation = findViewById<com.google.android.material.bottomnavigation.BottomNavigationView>(R.id.bottomNavigation)
        bottomNavigation?.setOnItemSelectedListener { item ->
            containerHome?.visibility = View.GONE
            containerCategories?.visibility = View.GONE
            containerCoupons?.visibility = View.GONE
            containerStores?.visibility = View.GONE
            containerProfile?.visibility = View.GONE
            
            when (item.itemId) {
                R.id.nav_home -> containerHome?.visibility = View.VISIBLE
                R.id.nav_categories -> containerCategories?.visibility = View.VISIBLE
                R.id.nav_coupons -> containerCoupons?.visibility = View.VISIBLE
                R.id.nav_stores -> containerStores?.visibility = View.VISIBLE
                R.id.nav_profile -> containerProfile?.visibility = View.VISIBLE
            }
            true
        }
"""
if "containerHome = findViewById" not in content:
    content = content.replace("vpBanner    = findViewById(R.id.vpBanner)", "vpBanner    = findViewById(R.id.vpBanner)\n" + init_views_add)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("MainActivity.kt patched with tab switching logic.")
