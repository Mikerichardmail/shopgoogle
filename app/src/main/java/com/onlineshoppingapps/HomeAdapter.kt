package com.onlineshoppingapps

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.ImageView
import android.widget.TextView
import android.util.Log
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.viewpager2.widget.ViewPager2

class HomeAdapter(
    private val stores: List<Store>,
    private val coupons: List<Coupon>,
    private val onStoreClick: (Store) -> Unit,
    private val onViewAllClick: (Int) -> Unit
) : RecyclerView.Adapter<RecyclerView.ViewHolder>() {

    companion object {
        const val TYPE_HEADER = 0
        const val TYPE_SEARCH = 1
        const val TYPE_BANNER = 2
        const val TYPE_TITLE = 3
        const val TYPE_STORE_GRID = 4
        const val TYPE_COUPON_LIST = 5
    }

    private val bannerImages = listOf(
        "https://raw.githubusercontent.com/Mikerichardmail/app-banners/main/photo_001.jpg",
        "https://raw.githubusercontent.com/Mikerichardmail/app-banners/main/photo_002.jpg",
        "https://raw.githubusercontent.com/Mikerichardmail/app-banners/main/photo_003.jpg"
    )

    override fun getItemViewType(position: Int): Int {
        return when (position) {
            0 -> TYPE_HEADER
            1 -> TYPE_SEARCH
            2 -> TYPE_BANNER
            3 -> TYPE_TITLE // "Popular Stores"
            4 -> TYPE_STORE_GRID
            5 -> TYPE_TITLE // "Latest Coupons"
            6 -> TYPE_COUPON_LIST
            else -> TYPE_TITLE
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        return try {
            when (viewType) {
                TYPE_HEADER -> HeaderViewHolder(inflater.inflate(R.layout.item_home_header, parent, false))
                TYPE_SEARCH -> SearchViewHolder(inflater.inflate(R.layout.item_home_search, parent, false))
                TYPE_BANNER -> BannerViewHolder(inflater.inflate(R.layout.item_home_banner_container, parent, false))
                TYPE_TITLE -> TitleViewHolder(inflater.inflate(R.layout.item_home_title, parent, false))
                TYPE_STORE_GRID -> GridViewHolder(inflater.inflate(R.layout.item_home_recycler, parent, false))
                TYPE_COUPON_LIST -> ListViewHolder(inflater.inflate(R.layout.item_home_recycler, parent, false))
                else -> TitleViewHolder(inflater.inflate(R.layout.item_home_title, parent, false))
            }
        } catch (e: Exception) {
            Log.e("SAVEKARO", "ViewHolder creation failed for type $viewType", e)
            val fallback = View(parent.context)
            fallback.layoutParams = ViewGroup.LayoutParams(0, 0)
            object : RecyclerView.ViewHolder(fallback) {}
        }
    }

    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        try {
            when (holder) {
                is BannerViewHolder -> {
                    holder.vpBanner?.let { vp ->
                        if (vp.adapter == null) {
                            vp.adapter = BannerAdapter(bannerImages)
                        }
                    }
                }
                is TitleViewHolder -> {
                    holder.tvTitle?.text = if (position == 3) "Popular Stores" else "Latest Coupons"
                    holder.tvViewAll?.setOnClickListener { onViewAllClick(position) }
                }
                is GridViewHolder -> {
                    holder.rv?.let { rv ->
                        val storesToDisplay = stores.take(12)
                        if (rv.adapter == null) {
                            rv.layoutManager = GridLayoutManager(rv.context, 4)
                            rv.adapter = StoreAdapter(storesToDisplay, onStoreClick, { _, _ -> })
                        } else {
                            (rv.adapter as? StoreAdapter)?.updateList(storesToDisplay)
                        }
                    }
                }
                is ListViewHolder -> {
                    holder.rv?.let { rv ->
                        if (rv.adapter == null) {
                            rv.layoutManager = LinearLayoutManager(rv.context)
                            rv.adapter = CouponAdapter(coupons)
                        } else {
                            (rv.adapter as? CouponAdapter)?.updateData(coupons)
                        }
                    }
                }
            }
        } catch (e: Exception) {
            Log.e("SAVEKARO", "Bind failed at position $position", e)
        }
    }

    override fun getItemCount(): Int = 7

    class HeaderViewHolder(view: View) : RecyclerView.ViewHolder(view)
    class SearchViewHolder(view: View) : RecyclerView.ViewHolder(view)
    
    class BannerViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val vpBanner: ViewPager2? = try {
            (view as? ViewPager2) ?: view.findViewById(R.id.vpBannerHome)
        } catch (e: Exception) { null }
    }
    
    class TitleViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val tvTitle: TextView? = try { view.findViewById(R.id.tvHomeTitle) } catch (e: Exception) { null }
        val tvViewAll: TextView? = try { view.findViewById(R.id.tvViewAll) } catch (e: Exception) { null }
    }
    
    class GridViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val rv: RecyclerView? = try {
            (view as? RecyclerView) ?: view.findViewById(R.id.rvHomeInner)
        } catch (e: Exception) { null }
    }
    
    class ListViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val rv: RecyclerView? = try {
            (view as? RecyclerView) ?: view.findViewById(R.id.rvHomeInner)
        } catch (e: Exception) { null }
    }
}
