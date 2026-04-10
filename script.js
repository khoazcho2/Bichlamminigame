// Supabase ESM import for GitHub Pages compatibility
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const SUPABASE_URL = 'https://huhyetvefyhlhyldkvis.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_40AA8unUr1HLIcgBn4gkFg_dvmCshjR';
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

let allLinks = [];
let categories = ['Tất cả'];

// Load links from 'link' table
async function loadLinks() {
  try {
    const { data, error } = await supabase
      .from('link')
      .select('id, title, url, category, created_at')
      .order('created_at', { ascending: false });

    if (error) throw error;

    allLinks = data || [];
    // Build unique categories
    const uniqueCats = [...new Set(allLinks.map(link => link.category).filter(Boolean))];
    categories = ['Tất cả', ...uniqueCats];

    console.log(`✅ Loaded ${allLinks.length} links, categories:`, categories);
    return true;
  } catch (error) {
    console.error('❌ Load error:', error.message);
    allLinks = [];
    return false;
  }
}

// Render links (filtered)
function renderLinks(links, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (!links || links.length === 0) {
    container.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">📭 Không có link nào. <a href="admin.html" target="_blank">Vào Admin thêm</a></p>';
    return;
  }

  container.innerHTML = links.map(link => `
    <div class="resource-card">
      <div class="resource-content">
        <span class="resource-category">${link.category || 'Khác'}</span>
        <h3 class="resource-title">${link.title || 'Không có tiêu đề'}</h3>
        ${link.url ? `<a href="${link.url}" target="_blank" class="download-btn">📥 Mở Link</a>` : '<p style="color: red;">❌ URL không hợp lệ</p>'}
        <small>Thêm: ${new Date(link.created_at).toLocaleDateString('vi-VN')}</small>
      </div>
    </div>
  `).join('');
}

// Filter & search
function filterLinks(searchTerm = '', selectedCategory = 'Tất cả') {
  return allLinks.filter(link => {
    const matchesSearch = !searchTerm || 
      (link.title?.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (link.url?.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (link.category?.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'Tất cả' || link.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });
}

// Render category filter (dynamic)
function renderCategoryFilter() {
  const select = document.getElementById('categoryFilter');
  if (select) {
    select.innerHTML = categories.map(cat => `<option value="${cat}">${cat}</option>`).join('');
  }
}

// Perform search/filter
function performSearch() {
  const searchTerm = document.getElementById('searchInput')?.value || '';
  const category = document.getElementById('categoryFilter')?.value || 'Tất cả';
  const filtered = filterLinks(searchTerm, category);
  renderLinks(filtered, 'resourcesGrid');
}

// ADMIN-specific functions
let isAdmin = false;

function initAdmin() {
  isAdmin = true;
}

// Load & render for admin list
async function loadAdminResources() {
  const success = await loadLinks();
  if (success) {
    renderAdminList(allLinks);
  } else {
    document.getElementById('resourcesList').innerHTML = '<p style="color: red;">❌ Lỗi tải dữ liệu. Kiểm tra Supabase table "link" và RLS.</p>';
  }
}

function renderAdminList(links) {
  const container = document.getElementById('resourcesList');
  if (!container) return;
  if (links.length === 0) {
    container.innerHTML = '<p style="text-align: center;">📭 Chưa có link. Thêm mới!</p>';
    return;
  }
  container.innerHTML = links.map(link => `
    <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
      <h3>${link.title || 'No title'}</h3>
      <a href="${link.url}" target="_blank" style="color: #007bff; word-break: break-all; display: block;">🔗 ${link.url}</a>
      <p><strong>Danh mục:</strong> ${link.category || 'Khác'}</p>
      <div style="margin-top: 1rem;">
        <button onclick="editItem('${link.id}')" style="background: #007bff; color: white; padding: 0.5rem 1rem; border: none; border-radius: 5px; margin-right: 0.5rem; cursor: pointer;">Sửa</button>
        <button onclick="deleteItem('${link.id}')" style="background: #dc3545; color: white; padding: 0.5rem 1rem; border: none; border-radius: 5px; cursor: pointer;">Xóa</button>
      </div>
    </div>
  `).join('');
}

// Delete item
async function deleteItem(id) {
  if (!confirm('Xóa link này?')) return;
  try {
    const { error } = await supabase.from('link').delete().eq('id', id);
    if (!error) {
      await loadAdminResources();
    } else {
      alert('❌ Lỗi xóa: ' + error.message);
    }
  } catch (error) {
    alert('❌ Lỗi: ' + error.message);
  }
}

// Edit placeholder
function editItem(id) {
  alert('Chức năng sửa đang được phát triển!');
}

// Init for main page
async function initMain() {
  await loadLinks();
  renderCategoryFilter();
  performSearch(); // Initial render
  setInterval(loadLinks, 30000); // Auto refresh every 30s
}

// Global init
window.addEventListener('load', async () => {
  if (window.location.pathname.includes('admin.html')) {
    initAdmin();
  } else {
    await initMain();
  }
});

