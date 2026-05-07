
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.39.7'

const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!!
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!!

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

function slugify(text: string) {
  return text.toLowerCase().replace(/[^a-z0-9_]/g, '').replace(/\s+/g, '_').replace(/-/g, '_')
}

Deno.serve(async (req) => {
  try {
    console.log("Fetching stores...")
    const { data: stores, error: storesError } = await supabase
      .from('stores')
      .select('id, name, domain, category, logo_url, affiliate_link, affiliate_url')
      .eq('active', true)
    
    if (storesError) throw storesError

    console.log("Fetching coupons...")
    const { data: coupons, error: couponsError } = await supabase
      .from('coupons')
      .select('code, title, description, success_score, store_id')
      .eq('status', 'active')

    if (couponsError) throw couponsError

    // Group coupons by store_id
    const storeCoupons: Record<string, any[]> = {}
    coupons.forEach(c => {
      if (!storeCoupons[c.store_id]) storeCoupons[c.store_id] = []
      storeCoupons[c.store_id].push(c)
    })

    // Merge data
    const finalData = stores.map(s => ({
      ...s,
      slug: slugify(s.name),
      coupons: storeCoupons[s.id] || [],
      final_link: s.affiliate_link || s.affiliate_url || `https://${s.domain}`,
      category_list: (s.category || 'Shopping').split(',').map((c: string) => c.trim())
    }))

    // Upload to Storage
    console.log("Uploading to Storage...")
    const { error: uploadError } = await supabase.storage
      .from('app-data')
      .upload('stores_data.json', JSON.stringify(finalData), {
        contentType: 'application/json',
        upsert: true
      })

    if (uploadError) throw uploadError

    return new Response(JSON.stringify({ success: true, count: finalData.length }), {
      headers: { "Content-Type": "application/json" },
    })
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { 
      status: 500,
      headers: { "Content-Type": "application/json" }
    })
  }
})
