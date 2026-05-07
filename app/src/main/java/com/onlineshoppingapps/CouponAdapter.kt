package com.onlineshoppingapps

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.recyclerview.widget.RecyclerView

import com.bumptech.glide.Glide

class CouponAdapter(private var coupons: List<Coupon>) : RecyclerView.Adapter<CouponAdapter.CouponViewHolder>() {

    class CouponViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val ivStoreLogo: ImageView = view.findViewById(R.id.ivStoreLogo)
        val tvStoreName: TextView = view.findViewById(R.id.tvStoreName)
        val tvCouponTitle: TextView = view.findViewById(R.id.tvCouponTitle)
        val tvCategory: TextView = view.findViewById(R.id.tvCategory)
        val tvCode: TextView = view.findViewById(R.id.tvCode)
        val btnCopy: Button = view.findViewById(R.id.btnCopy)
        val tvExpiry: TextView = view.findViewById(R.id.tvExpiry)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CouponViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_coupon, parent, false)
        return CouponViewHolder(view)
    }

    override fun onBindViewHolder(holder: CouponViewHolder, position: Int) {
        val coupon = coupons[position]
        holder.tvStoreName.text = coupon.storeName
        holder.tvCouponTitle.text = coupon.title
        holder.tvCategory.text = coupon.category
        holder.tvCode.text = coupon.code
        holder.tvExpiry.text = coupon.expiryDate

        // Load Store Icon
        val context = holder.itemView.context
        try {
            when {
                coupon.storeIconRes != 0 && coupon.storeIconRes != R.drawable.ic_store_nav -> {
                    Glide.with(context)
                        .load(coupon.storeIconRes)
                        .placeholder(R.drawable.ic_store_nav)
                        .error(R.drawable.ic_store_nav)
                        .into(holder.ivStoreLogo)
                }
                coupon.storeIconUrl.isNotEmpty() -> {
                    Glide.with(context)
                        .load(coupon.storeIconUrl)
                        .placeholder(R.drawable.ic_store_nav)
                        .error(R.drawable.ic_store_nav)
                        .into(holder.ivStoreLogo)
                }
                else -> {
                    holder.ivStoreLogo.setImageResource(R.drawable.ic_store_nav)
                }
            }
        } catch (e: Exception) {
            holder.ivStoreLogo.setImageResource(R.drawable.ic_store_nav)
        }

        holder.btnCopy.text = "COPY"
        holder.btnCopy.setOnClickListener {
            if (holder.btnCopy.text == "COPY") {
                val clipboard = it.context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                val clip = ClipData.newPlainText("Coupon Code", coupon.code)
                clipboard.setPrimaryClip(clip)
                Toast.makeText(it.context, "Code ${coupon.code} copied!", Toast.LENGTH_SHORT).show()
                holder.btnCopy.text = "VISIT"
            } else {
                try {
                    if (coupon.storeLink.isNotEmpty()) {
                        val intent = android.content.Intent(it.context, StoreBrowserActivity::class.java)
                        intent.putExtra("TARGET_URL", coupon.storeLink)
                        it.context.startActivity(intent)
                    } else {
                        Toast.makeText(it.context, "Store link not available.", Toast.LENGTH_SHORT).show()
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
    }

    override fun getItemCount() = coupons.size

    fun updateData(newCoupons: List<Coupon>) {
        coupons = newCoupons
        notifyDataSetChanged()
    }
}
