package com.onlineshoppingapps

import android.content.Intent
import android.net.Uri
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide

class StoreAdapter(
    private var stores: List<Store>,
    private val onClick: (Store) -> Unit,
    private val onFavoriteClick: (Store, Int) -> Unit
) : RecyclerView.Adapter<StoreAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val tvName: TextView = view.findViewById(R.id.tvName)
        val ivIcon: ImageView = view.findViewById(R.id.ivIcon)
        val ivFavorite: ImageView = view.findViewById(R.id.ivFavorite)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_store, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        try {
            val store = stores[position]
            holder.tvName.text = store.name

            val context = holder.itemView.context

            // Load Icon
            try {
                when {
                    store.iconRes != 0 && store.iconRes != R.drawable.ic_store_nav ->
                        Glide.with(context).load(store.iconRes)
                            .placeholder(R.drawable.ic_store_nav)
                            .into(holder.ivIcon)
                    store.iconUrl.isNotEmpty() ->
                        Glide.with(context).load(store.iconUrl)
                            .placeholder(R.drawable.ic_store_nav)
                            .into(holder.ivIcon)
                    else ->
                        holder.ivIcon.setImageResource(R.drawable.ic_store_nav)
                }
            } catch (e: Exception) {
                holder.ivIcon.setImageResource(R.drawable.ic_store_nav)
            }

            // Favorite icon
            try {
                if (store.isFavorite) {
                    holder.ivFavorite.setImageResource(R.drawable.ic_heart)
                } else {
                    holder.ivFavorite.setImageResource(R.drawable.ic_heart_outline)
                }
            } catch (_: Exception) {}

            holder.ivFavorite.setOnClickListener {
                try { onFavoriteClick(store, holder.adapterPosition) } catch (_: Exception) {}
            }

            // Scale animation on press
            holder.itemView.setOnClickListener {
                try {
                    it.animate().scaleX(0.95f).scaleY(0.95f).setDuration(80).withEndAction {
                        it.animate().scaleX(1f).scaleY(1f).setDuration(80).start()
                        try { onClick(store) } catch (_: Exception) {}
                    }.start()
                } catch (_: Exception) {
                    try { onClick(store) } catch (_: Exception) {}
                }
            }
        } catch (_: Exception) {
            // If anything crashes during bind, silently ignore for this item
        }
    }

    override fun getItemCount() = stores.size

    fun updateList(newList: List<Store>) {
        stores = newList
        notifyDataSetChanged()
    }
}

class CategoryAdapter(
    private var categories: List<Category>,
    private val onItemClick: (Category) -> Unit
) : RecyclerView.Adapter<CategoryAdapter.CategoryViewHolder>() {

    class CategoryViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val tvCatName: TextView = view.findViewById(R.id.tvCatName)
        val ivCatIcon: ImageView = view.findViewById(R.id.ivCatIcon)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CategoryViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_category_modern, parent, false)
        return CategoryViewHolder(view)
    }

    override fun onBindViewHolder(holder: CategoryViewHolder, position: Int) {
        val cat = categories[position]
        holder.tvCatName.text = cat.name
        
        val iconRes = when {
            cat.name.contains("Electronic", true) -> R.drawable.ic_electronics
            cat.name.contains("Beauty", true) -> R.drawable.ic_beauty
            cat.name.contains("Fashion", true) -> R.drawable.ic_fashion
            cat.name.contains("Health", true) -> R.drawable.ic_health
            cat.name.contains("Home", true) -> R.drawable.ic_home
            cat.name.contains("Kid", true) -> R.drawable.ic_kids
            cat.name.contains("Deal", true) -> R.drawable.ic_deals
            else -> R.drawable.ic_category
        }
        holder.ivCatIcon.setImageResource(iconRes)

        val gradientRes = when {
            cat.name.contains("Fashion", true) -> R.drawable.cat_fashion_gradient
            cat.name.contains("Beauty", true) -> R.drawable.cat_beauty_gradient
            cat.name.contains("Electronic", true) -> R.drawable.cat_electronics_gradient
            cat.name.contains("Health", true) -> R.drawable.cat_health_gradient
            cat.name.contains("Home", true) -> R.drawable.cat_home_gradient
            cat.name.contains("Kid", true) -> R.drawable.cat_food_gradient // Using food for kids as proxy
            cat.name.contains("Deal", true) -> R.drawable.cat_more_gradient
            else -> R.drawable.cat_more_gradient
        }
        
        try {
            val vGradient = holder.itemView.findViewById<View>(R.id.vGradientOverlay)
            vGradient?.setBackgroundResource(gradientRes)
        } catch (_: Exception) {}
        
        holder.itemView.setOnClickListener { onItemClick(cat) }
    }

    override fun getItemCount() = categories.size

    fun updateList(newList: List<Category>) {
        categories = newList
        notifyDataSetChanged()
    }
}

class QuickDealAdapter(
    private val deals: List<QuickDeal>,
    private val onClick: (QuickDeal) -> Unit
) : RecyclerView.Adapter<QuickDealAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val tvTitle: TextView = view.findViewById(R.id.tvTitle)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_quick_deal, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.tvTitle.text = deals[position].title
        holder.itemView.setOnClickListener { onClick(deals[position]) }
    }

    override fun getItemCount() = deals.size
}

class DealAdapter(
    private var deals: List<Deal>,
    private val onClick: (Deal) -> Unit
) : RecyclerView.Adapter<DealAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val tvTitle: TextView = view.findViewById(R.id.tvTitle)
        val btnLink: Button = view.findViewById(R.id.btnLink)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_deal, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.tvTitle.text = deals[position].title
        holder.btnLink.setOnClickListener { onClick(deals[position]) }
        holder.itemView.setOnClickListener { onClick(deals[position]) }
    }

    override fun getItemCount() = deals.size

    fun updateList(newList: List<Deal>) {
        deals = newList
        notifyDataSetChanged()
    }
}

class BannerAdapter(
    private val images: List<String>
) : RecyclerView.Adapter<BannerAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val ivBanner: ImageView = view.findViewById(R.id.ivBanner)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_banner, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        try {
            Glide.with(holder.itemView.context)
                .load(images[position])
                .placeholder(android.R.color.darker_gray)
                .error(android.R.color.darker_gray)
                .into(holder.ivBanner)
        } catch (_: Exception) {}
    }

    override fun getItemCount() = images.size
}
