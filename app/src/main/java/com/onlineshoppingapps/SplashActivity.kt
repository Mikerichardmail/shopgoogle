package com.onlineshoppingapps

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import android.view.animation.AnimationUtils
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.ImageView
import android.widget.LinearLayout
import androidx.appcompat.app.AppCompatActivity

class SplashActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)

        val ivIcon = findViewById<ImageView>(R.id.ivSplashIcon)
        val llTitle = findViewById<LinearLayout>(R.id.llSplashTitle)
        val tvTagline = findViewById<TextView>(R.id.tvSplashTagline)
        val progressBar = findViewById<ProgressBar>(R.id.progressSplash)
        val tvStatus = findViewById<TextView>(R.id.tvLoadingStatus)

        // Animate icon in
        ivIcon.animate().alpha(1f).scaleX(1.05f).scaleY(1.05f).setDuration(500)
            .withEndAction {
                ivIcon.animate().scaleX(1f).scaleY(1f).setDuration(200).start()
            }.start()

        // Stagger in title and other elements
        Handler(Looper.getMainLooper()).postDelayed({
            llTitle.animate().alpha(1f).translationY(0f).setDuration(400).start()
        }, 300)

        Handler(Looper.getMainLooper()).postDelayed({
            tvTagline.animate().alpha(1f).setDuration(300).start()
        }, 500)

        Handler(Looper.getMainLooper()).postDelayed({
            progressBar.animate().alpha(1f).setDuration(300).start()
            tvStatus.animate().alpha(1f).setDuration(300).start()
        }, 700)

        // Update status text while "loading"
        Handler(Looper.getMainLooper()).postDelayed({
            tvStatus.text = "Fetching latest coupons..."
        }, 1200)

        Handler(Looper.getMainLooper()).postDelayed({
            tvStatus.text = "Almost ready..."
        }, 2000)

        // Launch MainActivity after 2.5 seconds
        Handler(Looper.getMainLooper()).postDelayed({
            startActivity(Intent(this, MainActivity::class.java))
            overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out)
            finish()
        }, 2500)
    }
}
