package com.onlineshoppingapps

import android.os.Bundle
import android.util.Log
import android.view.MotionEvent
import android.view.View
import android.webkit.WebView
import android.widget.FrameLayout
import android.webkit.WebViewClient
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import org.json.JSONArray
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URI
import java.net.URL
import kotlin.concurrent.thread

class StoreBrowserActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private lateinit var cvCoupons: CardView
    private lateinit var rvCoupons: RecyclerView
    private lateinit var ivCloseCoupons: ImageView
    private lateinit var ivMinimizeCoupons: ImageView
    private lateinit var flFloatingWidget: FrameLayout
    private lateinit var ivFloatingIcon: ImageView
    private lateinit var ivCloseFloating: ImageView

    private var dX = 0f
    private var dY = 0f

    private var lastFetchedDomain = ""

    private var allStores = mutableListOf<Store>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_store_browser)

        webView = findViewById(R.id.webView)
        cvCoupons = findViewById(R.id.cvCoupons)
        rvCoupons = findViewById(R.id.rvCoupons)
        ivCloseCoupons = findViewById(R.id.ivCloseCoupons)
        ivMinimizeCoupons = findViewById(R.id.ivMinimizeCoupons)
        flFloatingWidget = findViewById(R.id.flFloatingWidget)
        ivFloatingIcon = findViewById(R.id.ivFloatingIcon)
        ivCloseFloating = findViewById(R.id.ivCloseFloating)

        ivCloseCoupons.setOnClickListener {
            cvCoupons.visibility = View.GONE
        }

        ivMinimizeCoupons.setOnClickListener {
            cvCoupons.visibility = View.GONE
            flFloatingWidget.visibility = View.VISIBLE
        }

        ivCloseFloating.setOnClickListener {
            flFloatingWidget.visibility = View.GONE
        }

        var startX = 0f
        var startY = 0f

        ivFloatingIcon.setOnTouchListener { _, event ->
            when (event.actionMasked) {
                MotionEvent.ACTION_DOWN -> {
                    dX = flFloatingWidget.x - event.rawX
                    dY = flFloatingWidget.y - event.rawY
                    startX = event.rawX
                    startY = event.rawY
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    flFloatingWidget.x = event.rawX + dX
                    flFloatingWidget.y = event.rawY + dY
                    true
                }
                MotionEvent.ACTION_UP -> {
                    if (Math.abs(event.rawX - startX) < 10 && Math.abs(event.rawY - startY) < 10) {
                        flFloatingWidget.visibility = View.GONE
                        cvCoupons.visibility = View.VISIBLE
                    }
                    true
                }
                else -> false
            }
        }

        rvCoupons.layoutManager = LinearLayoutManager(this)
        loadLocalData()

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                super.onPageStarted(view, url, favicon)
                url?.let { checkAndFetch(it) }
            }
        }

        val targetUrl = intent.getStringExtra("TARGET_URL")
        if (targetUrl != null) {
            webView.loadUrl(targetUrl)
        }
    }

    private fun checkAndFetch(urlStr: String) {
        try {
            val uri = URI(urlStr)
            var host = uri.host ?: return
            if (host.startsWith("www.")) {
                host = host.substring(4)
            }
            
            val shorteners = listOf("bitli.in", "ekaro.in", "fktr.in", "extp.in", "myntr.it", "ajiio.in", "bit.ly")
            if (shorteners.any { host.contains(it) }) return

            if (host != lastFetchedDomain) {
                lastFetchedDomain = host
                fetchCouponsForDomain(host)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun loadLocalData() {
        try {
            val cacheFile = java.io.File(filesDir, "stores_cache.json")
            val jsonString = if (cacheFile.exists()) {
                cacheFile.readText()
            } else {
                assets.open("stores_data.json").bufferedReader().use { it.readText() }
            }
            
            val array = JSONArray(jsonString)
            for (i in 0 until array.length()) {
                val obj = array.getJSONObject(i)
                val slug = obj.optString("slug")
                val name = obj.getString("name")
                val link = obj.getString("final_link")
                
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
                }

                val coupons = mutableListOf<Coupon>()
                val coupArray = obj.optJSONArray("coupons") ?: JSONArray()
                for (j in 0 until coupArray.length()) {
                    val cObj = coupArray.getJSONObject(j)
                    coupons.add(Coupon(
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

                allStores.add(Store(
                    id = obj.getString("id"),
                    name = name,
                    link = link,
                    categories = emptyList(),
                    iconUrl = obj.optString("logo_url"),
                    iconRes = iconRes,
                    cashback = "",
                    coupons = coupons
                ))
            }
            val distinctList = allStores.distinctBy { it.name.lowercase() }
            allStores.clear()
            allStores.addAll(distinctList)
        } catch (e: Exception) {
            Log.e("StoreBrowser", "Error loading local JSON", e)
        }
    }

    private fun fetchCouponsForDomain(domain: String) {
        val matchingStore = allStores.find { store ->
            val storeUri = URI(store.link)
            val storeHost = storeUri.host?.replace("www.", "")
            storeHost == domain || store.name.lowercase().contains(domain.lowercase())
        }

        if (matchingStore != null && matchingStore.coupons.isNotEmpty()) {
            runOnUiThread {
                rvCoupons.adapter = CouponAdapter(matchingStore.coupons)
                cvCoupons.visibility = View.VISIBLE
            }
        }
    }


    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
