// Admin password hash (double Base64 obfuscated)
const ADMIN_PW_HASH = 'aG9xdW9jZHoyMDE=';

// Load on admin
window.adminLogin = (input) => btoa(input) === ADMIN_PW_HASH;

// Supabase ESM for GitHub Pages
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const SUPABASE_URL = 'https://huhyetvefyhlhyldkvis.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_40AA8unUr1HLIcgBn4gkFg_dvmCshjR';
window.supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

let allLinks = [];
let categories = ['Tất cả'];

// Load links
async function loadLinks() {
  try {
    const { data, error } = await window.supabase
      .from('link')
      .select('id, title, url, category, created_at')
      .order('created_at', { ascending: false });

    if (error) throw error;

    allLinks = data || [];
    const uniqueCats = [...new Set(allLinks.map(link => link.category).filter(Boolean))];
    categories = ['Tất cả', ...uniqueCats];

    console.log(`✅ Loaded ${allLinks.length} links`);
    return true;
  } catch (error) {
    console.error('❌ Load error:', error.message);
    return false;
  }
}

// Render links
function renderLinks(links, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (!links?.length) {
    container.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">📭 Không có link. <a href="admin.html" target="_blank">Admin thêm</a></p>';
    return;
  }

  container.innerHTML = links.map(link => `
    <div class="resource-card">
      <div class="resource-content">
        <span class="resource-category">${link.category || 'Khác'}</span>
        <h3 class="resource-title">${link.title || 'No title'}</h3>
        ${link.url ? `<a href="${link.url}" target="_blank" class="download-btn">📥 Mở Link</a>` : '<p style="color: red;">❌ URL invalid</p>'}
        <small>${new Date(link.created_at).toLocaleDateString('vi-VN')}</small>
      </div>
    </div>
  `).join('');
}

// Filter
function filterLinks(search = '', category = 'Tất cả') {
  return allLinks.filter(link => {
    const term = search.toLowerCase();
    const matchesSearch = !term || 
      link.title?.toLowerCase().includes(term) ||
      link.url?.toLowerCase().includes(term) ||
      link.category?.toLowerCase().includes(term);
    const matchesCat = category === 'Tất cả' || link.category === category;
    return matchesSearch && matchesCat;
  });
}

// Category dropdown
function renderCategoryFilter() {
  const select = document.getElementById('categoryFilter');
  if (select) select.innerHTML = categories.map(c => `<option value="${c}">${c}</option>`).join('');
}

// Search/filter
function performSearch() {
  const search = document.getElementById('searchInput')?.value || '';
  const cat = document.getElementById('categoryFilter')?.value || 'Tất cả';
  renderLinks(filterLinks(search, cat), 'resourcesGrid');
}

// ADMIN functions
async function loadAdminResources() {
  const success = await loadLinks();
  const list = document.getElementById('resourcesList');
  if (success && list) renderAdminList(allLinks);
  else if (list) list.innerHTML = '<p style="color: red;">❌ Lỗi DB - check Supabase "link" table/RLS</p>';
}

function renderAdminList(links) {
  const list = document.getElementById('resourcesList');
  if (!list) return;
  if (!links?.length) {
    list.innerHTML = '<p style="text-align: center;">📭 No links. Add new!</p>';
    return;
  }
  list.innerHTML = links.map(link => `
    <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
      <h3>${link.title || 'No title'}</h3>
      <a href="${link.url}" target="_blank" style="color: #007bff; word-break: break-all;">🔗 ${link.url}</a>
      <p><strong>Cat:</strong> ${link.category || 'Other'}</p>
      <div style="margin-top: 1rem;">
        <button onclick="editItem('${link.id}')" style="background: #007bff; color: white; padding: 0.5rem 1rem; border: none; border-radius: 5px; margin-right: 0.5rem;">Edit</button>
        <button onclick="deleteItem('${link.id}')" style="background: #dc3545; color: white; padding: 0.5rem 1rem; border: none; border-radius: 5px;">Delete</button>
      </div>
    </div>
  `).join('');
}

async function deleteItem(id) {
  if (!confirm('Delete?')) return;
  try {
    const { error } = await window.supabase.from('link').delete().eq('id', id);
    if (!error) await loadAdminResources();
    else alert('Delete error: ' + error.message);
  } catch (e) {
    alert('Error: ' + e.message);
  }
}

function editItem(id) {
  alert('Edit coming soon!');
}

// Init
async function initMain() {
  await loadLinks();
  renderCategoryFilter();
  performSearch();
  setInterval(loadLinks, 30000);
}



// Global load
window.addEventListener('load', async () => {
  if (window.location.pathname.includes('admin.html')) {
    // Admin pw check in admin.html inline JS
  } else {
    await initMain();
  }
});

// Admin addLink function (called from admin.html)
async function addLink() {
  const title = document.getElementById("title").value;
  const url = document.getElementById("url").value;
  const category = document.getElementById("category").value;

  if (!title || !url) {
    alert('Điền đầy đủ!');
    return;
  }

  try {
    const { data, error } = await window.supabase
      .from("link")
      .insert([{ title, url, category }]);

    if (error) throw error;

    alert("✅ Thêm thành công!");
    document.getElementById("title").value = '';
    document.getElementById("url").value = '';
    await loadAdminResources();  // Reload list
  } catch (error) {
    alert("❌ " + error.message);
  }
}


