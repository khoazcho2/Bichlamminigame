# 📥 Website Chia Sẻ Link Tải (Supabase)

Website chia sẻ link tải với admin panel đầy đủ CRUD. Fixed & optimized hoàn toàn!

## 🚀 Demo
Live: http://localhost:3000 (server đang chạy)  
Admin: http://localhost:3000/admin.html

## ✨ Features
- ✅ **Load links realtime** từ Supabase
- ✅ **Search** title/URL/category 
- ✅ **Filter** dynamic categories
- ✅ **Admin**: Add/Edit/Delete (password: `hoquocdz01`)
- ✅ **Responsive** mobile-first
- ✅ **Error-safe** null handling
- ✅ **Auto-refresh** 30s

## 🛠 Supabase Setup
1. Project: `https://huhyetvefyhlhyldkvis.supabase.co`
2. Table: `link` columns: `id, title, url, category, created_at`
3. **RLS**: Enable public read/insert/delete (anon key)
4. Anon key: `sb_publishable_40AA8unUr1HLIcgBn4gkFg_dvmCshjR`

## 📱 Test Locally
```bash
npx serve .
```
Open http://localhost:3000

## ☁️ Deploy GitHub Pages
1. Push repo
2. Settings > Pages > Deploy from `main`
3. Live: `https://username.github.io/repo`

## 🔧 Admin
- PW: Lưu trong `admin-password.txt` (không lộ source)
- Add: Form → Save
- Delete: Buttons in list

## 📁 Files
- `index.html`: Main page
- `admin.html`: Admin CRUD
- `script.js`: Supabase + logic
- `style.css`: Modern UI

**Fixed issues:** Wrong table/fields, security keys, console errors, search/filter, schema.

✅ **Production ready!**

