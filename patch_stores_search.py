import os

file_path = r"f:\online shoping apps new\app\src\main\java\com\onlineshoppingapps\MainActivity.kt"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

stores_search_logic = """
        val etSearchStores = findViewById<EditText>(R.id.etSearchStores)
        val btnFavToggle = findViewById<TextView>(R.id.btnFavToggle)
        var showOnlyFavs = false

        fun filterAllStores() {
            val query = etSearchStores?.text?.toString()?.trim() ?: ""
            var filtered = allStores

            if (showOnlyFavs) {
                filtered = filtered.filter { it.isFavorite }
            }

            if (query.isNotEmpty()) {
                filtered = filtered.filter {
                    it.name.contains(query, ignoreCase = true) ||
                    it.categories.any { cat -> cat.contains(query, ignoreCase = true) }
                }
            }

            (rvAllStores?.adapter as? StoreAdapter)?.updateList(filtered)
        }

        etSearchStores?.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                filterAllStores()
            }
            override fun afterTextChanged(s: Editable?) {}
        })

        btnFavToggle?.setOnClickListener {
            showOnlyFavs = !showOnlyFavs
            if (showOnlyFavs) {
                btnFavToggle.setBackgroundResource(R.drawable.bg_search)
                btnFavToggle.backgroundTintList = android.content.res.ColorStateList.valueOf(android.graphics.Color.parseColor("#E91E63"))
                btnFavToggle.setTextColor(android.graphics.Color.WHITE)
            } else {
                btnFavToggle.setBackgroundResource(R.drawable.bg_search)
                btnFavToggle.backgroundTintList = android.content.res.ColorStateList.valueOf(android.graphics.Color.parseColor("#FFE4EC"))
                btnFavToggle.setTextColor(android.graphics.Color.parseColor("#E91E63"))
            }
            filterAllStores()
        }
"""

if "etSearchStores?.addTextChangedListener" not in content:
    # Insert it right after setting rvAllStores adapter
    content = content.replace("rvAllStores?.adapter?.notifyItemChanged(pos)\n        })", 
                              "rvAllStores?.adapter?.notifyItemChanged(pos)\n        })\n" + stores_search_logic)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Stores search logic added.")
