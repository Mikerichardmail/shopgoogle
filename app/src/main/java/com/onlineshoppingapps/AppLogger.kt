package com.onlineshoppingapps

import android.os.Handler
import android.os.Looper
import android.widget.TextView
import java.util.*

object AppLogger {
    private val logs = LinkedList<String>()
    private var debugTextView: TextView? = null

    fun log(message: String) {
        val timestamp = java.text.SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(Date())
        val formatted = "[$timestamp] $message"
        logs.add(formatted)
        if (logs.size > 50) logs.removeFirst()
        
        android.util.Log.d("APP_DEBUG", formatted)
        
        Handler(Looper.getMainLooper()).post {
            debugTextView?.text = logs.joinToString("\n")
        }
    }

    fun setView(textView: TextView) {
        debugTextView = textView
        debugTextView?.text = logs.joinToString("\n")
    }
}
