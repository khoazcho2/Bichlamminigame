// API config
const API_BASE = 'http://localhost:3000/api';
let resources = [];
const defaultCategories = ['Tất cả', 'Game', 'Tool', 'Phần mềm', 'Tài liệu'];

// Khởi tạo
async function init() {
  await fetchResources();
  renderCategories();
  renderResources();
}

// Fetch from API
async function fetchResources() {
  try {
    const res = await fetch(`${API_BASE}/resources`);
    if (res.ok) {
      resources = await res.json();
    } else {
      console.error('API error:', res.statusText);
      document.getElementById('resourcesGrid').innerHTML = '<p style="text-align:center;">Server chưa chạy hoặc lỗi API. Vào <a href="admin.html">Admin</a> kiểm tra.</p>';
    }
  } catch (err) {
    console.error('Server chưa chạy?', err);
    document.getElementById('resourcesGrid').innerHTML = '<p style="text-align:center;">Server chưa chạy. Chạy `npm start`.</p>';
  }
}

// Render categories
function renderCategories() {
  const select = document.getElementById('categoryFilter');
  select.innerHTML = defaultCategories.map(cat => `<option value="${cat}">${cat}</option>`).join('');
}

// Render resources (user only)
function renderResources(filter = {}) {
  const grid = document.getElementById('resourcesGrid');
  let filtered = resources;

  if (filter.category && filter.category !== 'Tất cả') {
    filtered = filtered.filter(r => r.category === filter.category);
  }

  if (filter.search) {
    const term = filter.search.toLowerCase();
    filtered = filtered.filter(r => 
      r.title.toLowerCase().includes(term) || r.description.toLowerCase().includes(term)
    );
  }

  if (filtered.length === 0) {
    grid.innerHTML = '<p style="text-align:center; color:#666;">Không tìm thấy. Thử tìm khác hoặc thêm ở Admin.</p>';
    return;
  }

  grid.innerHTML = filtered.map(r => `
    <div class="resource-card">
      ${r.image ? `<img src="${r.image}" alt="${r.title}" class="resource-image">` : '<div class="resource-image" style="display:flex;align-items:center;justify-content:center;color:#999;">No image</div>'}
      <div class="resource-content">
        <span class="resource-category">${r.category}</span>
        <h3 class="resource-title">${r.title}</h3>
        <p class="resource-desc">${r.description}</p>
        <button class="download-btn" onclick="openLink('${r.url}')">📥 Tải / Mở Link</button>
      </div>
    </div>
  `).join('');
}

// Open link
function openLink(url) {
  window.open(url, '_blank');
}

// Search & filter
function performSearch() {
  const search = document.getElementById('searchInput').value;
  const category = document.getElementById('categoryFilter').value;
  renderResources({ search, category });
}

// Init on load
window.addEventListener('load', init);

// Auto refresh every 30s
setInterval(() => {
  fetchResources().then(() => renderResources({}));
}, 30000);
