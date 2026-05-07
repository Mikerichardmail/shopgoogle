package com.onlineshoppingapps

import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import android.os.Handler
import android.os.Looper
import android.content.Intent
import org.json.JSONArray
import kotlin.concurrent.thread
import java.net.URL

class MainActivity : AppCompatActivity() {

    private var containerCategories: View? = null
    private var containerCoupons: View? = null
    private var containerStores: View? = null
    private var containerSettings: View? = null

    private var allStores = mutableListOf<Store>()
    private var allCoupons = mutableListOf<Coupon>()

    private var storesAdapter: StoreAdapter? = null
    private var couponsAdapter: CouponAdapter? = null
    
    private val PREFS_NAME = "app_prefs"
    private val KEY_FAVORITES = "favorite_stores"
    private val KEY_LAST_CATEGORY = "last_visited_category"


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        try {
            setContentView(R.layout.activity_main)
            
            containerCategories = findViewById(R.id.containerCategories)
            containerCoupons = findViewById(R.id.containerCoupons)
            containerStores = findViewById(R.id.containerStores)
            containerSettings = findViewById(R.id.containerSettings)

            val bottomNav = findViewById<com.google.android.material.bottomnavigation.BottomNavigationView>(R.id.bottomNavigation)
            bottomNav?.selectedItemId = R.id.nav_stores
            
            bottomNav?.setOnItemSelectedListener { item ->
                hideAllContainers()
                when (item.itemId) {
                    R.id.nav_categories -> {
                        containerCategories?.visibility = View.VISIBLE
                        setupCategoryTab()
                    }
                    R.id.nav_coupons -> {
                        containerCoupons?.visibility = View.VISIBLE
                        setupCouponsTab()
                    }
                    R.id.nav_stores -> {
                        containerStores?.visibility = View.VISIBLE
                        setupStoresTab()
                    }
                    R.id.nav_settings -> {
                        containerSettings?.visibility = View.VISIBLE
                        setupSettingsTab()
                    }
                }
                true
            }

            loadInitialData()
            containerStores?.visibility = View.VISIBLE
            setupStoresTab()

        } catch (e: Exception) {
            Log.e("SHOPPING_APP", "Main Init Fail", e)
        }
    }

    private fun loadInitialData() {
        loadStoresFromJson()
        if (allStores.isEmpty()) {
            allStores.addAll(listOf(
                Store("amazon", "Amazon", "https://ekaro.in/enkr20250430s57418738", listOf("Electronics"), "https://www.google.com/s2/favicons?domain=amazon.in&sz=128", R.drawable.ic_new_amazon, "Up to 8% Cashback", listOf("Top", "All")),
                Store("flipkart", "Flipkart", "https://fktr.in/PjTHz0H", listOf("Electronics"), "https://www.google.com/s2/favicons?domain=flipkart.com&sz=128", R.drawable.ic_new_flipkart, "Up to 7% Cashback", listOf("Top", "All"))
            ))
        }
        // Background sync from Supabase Storage (Automated JSON)
        syncStoresFromNetwork()
    }

    private fun syncStoresFromNetwork() {
        val prefs = getSharedPreferences("app_prefs", MODE_PRIVATE)
        val lastSync = prefs.getLong("last_json_sync", 0L)
        val currentTime = System.currentTimeMillis()
        val fortyEightHours = 48 * 60 * 60 * 1000L // 48 hours in milliseconds

        if (currentTime - lastSync < fortyEightHours) {
            Log.d("SAVEKARO", "Skipping sync, last sync was less than 48 hours ago")
            return
        }

        thread {
            try {
                val url = URL("https://fwhzasbjexillgfrvksx.supabase.co/storage/v1/object/public/app-data/stores_data.json")
                val connection = url.openConnection() as java.net.HttpURLConnection
                connection.connectTimeout = 5000
                if (connection.responseCode == 200) {
                    val json = connection.inputStream.bufferedReader().use { it.readText() }
                    
                    // Save to internal storage
                    val file = java.io.File(filesDir, "stores_cache.json")
                    file.writeText(json)
                    
                    // Update sync timestamp
                    prefs.edit().putLong("last_json_sync", currentTime).apply()
                    
                    runOnUiThread {
                        loadStoresFromJson()
                        setupStoresTab()
                        if (containerCoupons?.visibility == View.VISIBLE) setupCouponsTab()
                    }
                    Log.d("SAVEKARO", "Network sync successful! Next sync in 48 hours.")
                }
            } catch (e: Exception) {
                Log.e("SAVEKARO", "Network sync failed", e)
            }
        }
    }


    private fun loadStoresFromJson() {
        try {
            // Priority: 1. Internal Cache, 2. Assets
            val cacheFile = java.io.File(filesDir, "stores_cache.json")
            val source: String
            val jsonString = if (cacheFile.exists()) {
                source = "Internal Cache"
                cacheFile.readText()
            } else {
                source = "Bundled Assets"
                assets.open("stores_data.json").bufferedReader().use { it.readText() }
            }
            
            val array = JSONArray(jsonString)
            val newStores = mutableListOf<Store>()
            val newCoupons = mutableListOf<Coupon>()
            var missingIconsCount = 0

            for (i in 0 until array.length()) {
                val obj = array.getJSONObject(i)
                val slug = obj.optString("slug")
                val name = obj.getString("name")
                val link = obj.getString("final_link")
                
                val categories = mutableListOf<String>()
                val catArray = obj.optJSONArray("category_list") ?: JSONArray()
                for (j in 0 until catArray.length()) categories.add(catArray.getString(j))

                val iconUrl = obj.optString("logo_url")
                
                var iconRes = 0
                val id = obj.getString("id")
                val safeId = id.replace("-", "_")
                
                // Try Slug first
                iconRes = resources.getIdentifier("ic_new_$slug", "drawable", packageName)
                
                // Try Slug with underscores
                if (iconRes == 0) {
                    val safeSlug = slug.replace("-", "_")
                    iconRes = resources.getIdentifier("ic_new_$safeSlug", "drawable", packageName)
                }
                
                // Try UUID
                if (iconRes == 0) {
                    iconRes = resources.getIdentifier("ic_new_$safeId", "drawable", packageName)
                }

                // Special case for tatacliq
                if (iconRes == 0 && slug == "tatacliq") {
                    iconRes = resources.getIdentifier("ic_new_tata_cliq", "drawable", packageName)
                }
                
                if (iconRes == 0) {
                    iconRes = R.drawable.ic_store_nav 
                    missingIconsCount++
                }

                val storeCoupons = mutableListOf<Coupon>()
                val coupArray = obj.optJSONArray("coupons") ?: JSONArray()
                for (j in 0 until coupArray.length()) {
                    val cObj = coupArray.getJSONObject(j)
                    storeCoupons.add(Coupon(
                        id = "", 
                        code = cObj.getString("code"),
                        title = cObj.getString("title"),
                        successScore = cObj.optInt("success_score", 100),
                        storeId = slug,
                        storeName = name,
                        storeIconRes = iconRes,
                        storeIconUrl = iconUrl,
                        storeLink = link
                    ))
                }
                newCoupons.addAll(storeCoupons)

                newStores.add(Store(
                    id = obj.getString("id"),
                    name = name,
                    link = link,
                    categories = categories,
                    iconUrl = iconUrl,
                    iconRes = iconRes,
                    cashback = "Up to 10% Cashback",
                    priority = obj.optInt("priority", obj.optInt("position", 999)),
                    coupons = storeCoupons
                ))
            }
            
            // Remove duplicates (by name)
            val distinctStores = newStores.distinctBy { it.name.lowercase() }.toMutableList()
            
            // Load favorites from prefs
            val favorites = getSharedPreferences(PREFS_NAME, MODE_PRIVATE).getStringSet(KEY_FAVORITES, emptySet()) ?: emptySet()
            distinctStores.forEach { it.isFavorite = favorites.contains(it.id) }

            // Apply custom sorting logic
            sortStores(distinctStores)

            allStores.clear()
            allStores.addAll(distinctStores)
            allCoupons.clear()
            allCoupons.addAll(newCoupons)
            
            Log.d("SAVEKARO_DEBUG", "--- DATA LOAD COMPLETE ---")
            Log.d("SAVEKARO_DEBUG", "Source: $source")
            Log.d("SAVEKARO_DEBUG", "Total Stores: ${allStores.size}")
            Log.d("SAVEKARO_DEBUG", "Total Coupons: ${allCoupons.size}")
            Log.d("SAVEKARO_DEBUG", "Stores with Missing Icons: $missingIconsCount")
            Log.d("SAVEKARO_DEBUG", "--------------------------")
            
        } catch (e: Exception) {
            Log.e("SAVEKARO", "Error loading local JSON", e)
        }
    }

    private fun setupStoresTab() {
        val rv = containerStores?.findViewById<RecyclerView>(R.id.rvAllStores)
        rv?.let {
            it.layoutManager = GridLayoutManager(this, 4)
            if (storesAdapter == null) {
                storesAdapter = StoreAdapter(allStores, { store -> 
                    openStore(store)
                }, { store, pos -> 
                    toggleFavorite(store)
                })
                it.adapter = storesAdapter
            } else {
                it.adapter = storesAdapter
            }
        }
        setupSearch()
    }

    private fun openStore(store: Store) {
        // Save last visited category
        val category = store.categories.firstOrNull()
        if (category != null) {
            getSharedPreferences(PREFS_NAME, MODE_PRIVATE).edit()
                .putString(KEY_LAST_CATEGORY, category)
                .apply()
        }
        
        // Re-sort to bring this category up next time
        sortStores(allStores)
        storesAdapter?.notifyDataSetChanged()
        
        openLink(store.link)
    }

    private fun toggleFavorite(store: Store) {
        val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        val favorites = prefs.getStringSet(KEY_FAVORITES, mutableSetOf())?.toMutableSet() ?: mutableSetOf()
        
        if (favorites.contains(store.id)) {
            favorites.remove(store.id)
            store.isFavorite = false
        } else {
            favorites.add(store.id)
            store.isFavorite = true
        }
        
        prefs.edit().putStringSet(KEY_FAVORITES, favorites).apply()
        
        // Re-sort and update
        sortStores(allStores)
        storesAdapter?.notifyDataSetChanged()
    }

    private fun sortStores(list: MutableList<Store>) {
        val lastCat = getSharedPreferences(PREFS_NAME, MODE_PRIVATE).getString(KEY_LAST_CATEGORY, "")
        
        list.sortWith(Comparator { s1, s2 ->
            // 1. Favorites first
            if (s1.isFavorite && !s2.isFavorite) return@Comparator -1
            if (!s1.isFavorite && s2.isFavorite) return@Comparator 1
            
            // 2. Last visited category stores second
            val s1InCat = lastCat != "" && s1.categories.contains(lastCat)
            val s2InCat = lastCat != "" && s2.categories.contains(lastCat)
            if (s1InCat && !s2InCat) return@Comparator -1
            if (!s1InCat && s2InCat) return@Comparator 1
            
            // 3. Then by Priority
            if (s1.priority != s2.priority) return@Comparator s1.priority - s2.priority
            
            // 4. Finally Alphabetical
            s1.name.lowercase().compareTo(s2.name.lowercase())
        })
    }

    private fun setupCouponsTab() {
        val rv = containerCoupons?.findViewById<RecyclerView>(R.id.rvAllCoupons)
        rv?.let {
            it.layoutManager = LinearLayoutManager(this)
            if (couponsAdapter == null) {
                couponsAdapter = CouponAdapter(allCoupons)
                it.adapter = couponsAdapter
            } else {
                it.adapter = couponsAdapter
            }
        }
        setupSearch()
    }

    private var isSearchSetup = false
    private fun setupSearch() {
        if (isSearchSetup) return
        isSearchSetup = true

        // Stores Search
        val etSearchStores = containerStores?.findViewById<android.widget.EditText>(R.id.etSearchStores)
        etSearchStores?.addTextChangedListener(object : android.text.TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                val query = s.toString().lowercase()
                val filtered = if (query.isEmpty()) allStores else allStores.filter { 
                    it.name.lowercase().contains(query) || it.categories.any { cat -> cat.lowercase().contains(query) }
                }.toMutableList()
                
                sortStores(filtered)
                storesAdapter?.updateList(filtered)
            }
            override fun afterTextChanged(s: android.text.Editable?) {}
        })

        // Coupons Search
        val etSearchCoupons = containerCoupons?.findViewById<android.widget.EditText>(R.id.etSearchCoupons)
        etSearchCoupons?.addTextChangedListener(object : android.text.TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                val query = s.toString().lowercase()
                val filtered = if (query.isEmpty()) allCoupons else allCoupons.filter { 
                    it.storeName.lowercase().contains(query) || it.title.lowercase().contains(query) || it.code.lowercase().contains(query)
                }
                couponsAdapter?.updateData(filtered)
            }
            override fun afterTextChanged(s: android.text.Editable?) {}
        })
    }

    private fun setupCategoryTab() {
        val root = containerCategories ?: return
        val rv = root.findViewById<RecyclerView>(R.id.rvCategories) ?: return
        val gridContainer = root.findViewById<View>(R.id.containerCategoryGrid)
        val storesContainer = root.findViewById<View>(R.id.containerCategoryStores)
        val rvStores = root.findViewById<RecyclerView>(R.id.rvCategorySpecificStores)
        val tvTitle = root.findViewById<TextView>(R.id.tvSelectedCategoryTitle)
        val ivBack = root.findViewById<ImageView>(R.id.ivBackFromCategory)

        if (rv.adapter != null) return
        rv.layoutManager = LinearLayoutManager(this)
        val categories = listOf("Fashion", "Beauty", "Electronics", "Health", "Home", "Kids", "Deals").map { Category(it) }
        
        rv.adapter = CategoryAdapter(categories) { cat ->
            // Filter stores
            val filteredStores = allStores.filter { it.categories.any { s -> s.contains(cat.name, true) } }
            
            // UI Switch
            gridContainer?.visibility = View.GONE
            storesContainer?.visibility = View.VISIBLE
            tvTitle?.text = cat.name
            
            // Setup Store Recycler
            rvStores?.layoutManager = GridLayoutManager(this, 4)
            rvStores?.adapter = StoreAdapter(filteredStores, { store -> openLink(store.link) }, { _, _ -> })
        }

        ivBack?.setOnClickListener {
            storesContainer?.visibility = View.GONE
            gridContainer?.visibility = View.VISIBLE
        }
    }

    private fun hideAllContainers() {
        containerCategories?.visibility = View.GONE
        containerCoupons?.visibility = View.GONE
        containerStores?.visibility = View.GONE
        containerSettings?.visibility = View.GONE
        
        // Reset category view state
        containerCategories?.findViewById<View>(R.id.containerCategoryGrid)?.visibility = View.VISIBLE
        containerCategories?.findViewById<View>(R.id.containerCategoryStores)?.visibility = View.GONE
    }
    
    private fun setupSettingsTab() {
        val root = containerSettings ?: return
        
        // Clear Cache
        root.findViewById<View>(R.id.btnClearCache)?.setOnClickListener {
            try {
                // Clear JSON Cache
                val cacheFile = java.io.File(filesDir, "stores_cache.json")
                if (cacheFile.exists()) cacheFile.delete()
                
                // Clear User Prefs (Favorites and History)
                getSharedPreferences(PREFS_NAME, MODE_PRIVATE).edit()
                    .remove(KEY_FAVORITES)
                    .remove(KEY_LAST_CATEGORY)
                    .apply()
                
                // Reset in-memory state
                allStores.forEach { it.isFavorite = false }
                sortStores(allStores)
                storesAdapter?.notifyDataSetChanged()
                
                android.widget.Toast.makeText(this, "Cache and preferences cleared", android.widget.Toast.LENGTH_SHORT).show()
                loadStoresFromJson() // Reload from assets
            } catch (e: Exception) {
                android.widget.Toast.makeText(this, "Error clearing cache", android.widget.Toast.LENGTH_SHORT).show()
            }
        }
        
        // Share App
        root.findViewById<View>(R.id.btnShareApp)?.setOnClickListener {
            val shareIntent = Intent(Intent.ACTION_SEND)
            shareIntent.type = "text/plain"
            shareIntent.putExtra(Intent.EXTRA_SUBJECT, "Download Online Shopping App")
            shareIntent.putExtra(Intent.EXTRA_TEXT, "Check out the Online Shopping App for the best deals and coupons: https://play.google.com/store/apps/details?id=$packageName")
            startActivity(Intent.createChooser(shareIntent, "Share via"))
        }
        
        // Rate Us
        root.findViewById<View>(R.id.btnRateUs)?.setOnClickListener {
            try {
                startActivity(Intent(Intent.ACTION_VIEW, android.net.Uri.parse("market://details?id=$packageName")))
            } catch (e: Exception) {
                startActivity(Intent(Intent.ACTION_VIEW, android.net.Uri.parse("https://play.google.com/store/apps/details?id=$packageName")))
            }
        }
        
        // Contact Us
        root.findViewById<View>(R.id.btnContactUs)?.setOnClickListener {
            val intent = Intent(Intent.ACTION_SENDTO)
            intent.data = android.net.Uri.parse("mailto:")
            intent.putExtra(Intent.EXTRA_EMAIL, arrayOf("support@onlineshoppingapps.com"))
            intent.putExtra(Intent.EXTRA_SUBJECT, "Feedback for Online Shopping App")
            if (intent.resolveActivity(packageManager) != null) {
                startActivity(intent)
            } else {
                android.widget.Toast.makeText(this, "No email app found", android.widget.Toast.LENGTH_SHORT).show()
            }
        }
        
        // Privacy & Terms
        root.findViewById<View>(R.id.btnPrivacy)?.setOnClickListener {
            startActivity(Intent(Intent.ACTION_VIEW, android.net.Uri.parse("https://savekaro.com/privacy")))
        }
        root.findViewById<View>(R.id.btnTerms)?.setOnClickListener {
            startActivity(Intent(Intent.ACTION_VIEW, android.net.Uri.parse("https://savekaro.com/terms")))
        }
        
        // Switches (Dummy implementation for now)
        root.findViewById<android.widget.Switch>(R.id.switchDarkMode)?.setOnCheckedChangeListener { _, isChecked ->
            android.widget.Toast.makeText(this, "Dark Mode: ${if (isChecked) "ON" else "OFF"}", android.widget.Toast.LENGTH_SHORT).show()
        }
    }


    private fun openLink(url: String) {
        if (url.isBlank()) return
        try {
            val intent = Intent(this, StoreBrowserActivity::class.java)
            intent.putExtra("TARGET_URL", url)
            startActivity(intent)
        } catch (_: Exception) {}
    }
}
