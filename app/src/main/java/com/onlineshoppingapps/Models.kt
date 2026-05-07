package com.onlineshoppingapps

data class Store(
    val id: String,
    val name: String,
    val link: String,
    val categories: List<String>,
    val iconUrl: String,
    val iconRes: Int = 0,
    val cashback: String = "",
    val tabs: List<String> = listOf("All"),
    var isFavorite: Boolean = false,
    val tags: List<String> = listOf(),
    var bgColor: Int? = null,
    val priority: Int = 999,
    val coupons: List<Coupon> = listOf()
)

data class Category(
    val name: String
)

data class Deal(
    val title: String,
    val link: String
)

data class QuickDeal(
    val title: String,
    val link: String
)

data class Coupon(
    val id: String,
    val code: String,
    val title: String,
    val successScore: Int,
    val storeId: String = "",
    val storeName: String = "",
    val storeIconRes: Int = 0,
    val storeIconUrl: String = "",
    val storeLink: String = "",
    val category: String = "Shopping",
    val expiryDate: String = "Expiring soon"
)
