// Supabase - USER VIEW (public)
const supabaseUrl = "https://huhyetvefyhlhyldkvis.supabase.co";
const supabaseKey = "sb_publishable_40AA8unUr1HLIcgBn4gkFg_dvmCshjR"; // User chỉ cần anon key

const supabaseClient = supabase.createClient(supabaseUrl, supabaseKey);

let resources = [];
const defaultCategories = ['Tất cả', 'Game', 'Tool', 'Phần mềm', 'Tài liệu'];

// Khởi tạo
async function init() {
  await loadLinks();
  renderCategories();
  renderResources();
}

// Load from "link" table
async function loadLinks() {
  const { data, error } = await supabaseClient
    .from("link")
    .select("*")
    .order("created_at", { ascending: false });

  if (error) {
    console.log(error);
    document.getElementById('resourcesGrid').innerHTML = '<p>Lỗi load. Admin thêm dữ liệu.</p>';
    return;
  }

  resources = data || [];
  console.log('Loaded', resources.length, 'links');
}

// Render categories  
function renderCategories() {
  const select = document.getElementById('categoryFilter');
  if (select) {
    select.innerHTML = defaultCategories.map(cat => `<option value="${cat}">${cat}</option>`).join('');
  }
}

// Render links
function renderResources(filter = {}) {
  const grid = document.getElementById('resourcesGrid');
  let filtered = resources;

  // Simple filter (add category field to table later)
  if (filter.search) {
    const term = filter.search.toLowerCase();
    filtered = filtered.filter(r => 
      (r.text || r.title || '').toLowerCase().includes(term) ||
      r.url.toLowerCase().includes(term)
    );
  }

  if (filtered.length === 0) {
    grid.innerHTML = '<p style="text-align:center;">Không tìm thấy link.</p>';
    return;
  }

  grid.innerHTML = filtered.map(r => `
    <div class="resource-card">
      <div class="resource-content">
        <h3 class="resource-title">${r.text || r.title || 'Link'}</h3>
        <a href="${r.url}" target="_blank" class="download-btn" style="display: block; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; text-align: center; border-radius: 5px; margin-top: 1rem;">📥 Mở Link</a>
      </div>
    </div>
  `).join('');
}

// Search
function performSearch() {
  const search = document.getElementById('searchInput')?.value || '';
  renderResources({ search });
}

// Init
window.addEventListener('load', init);
setInterval(loadLinks, 30000); // Auto refresh
