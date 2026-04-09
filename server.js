const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const PORT = 3000;
const DATA_FILE = path.join(__dirname, 'data.json');
const ADMIN_PASS = 'hoquocdz01';

app.use(cors());
app.use(express.json());
app.use(express.static('.')); // Serve static files: html, css, js

// Helper: read data
async function readData() {
  try {
    const data = await fs.readFile(DATA_FILE, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    return [];
  }
}

// Helper: write data
async function writeData(data) {
  await fs.writeFile(DATA_FILE, JSON.stringify(data, null, 2));
}

// GET /api/resources
app.get('/api/resources', async (req, res) => {
  const resources = await readData();
  res.json(resources);
});

// POST /api/resources (add)
app.post('/api/resources', async (req, res) => {
  const resources = await readData();
  const newResource = { id: Date.now().toString(), ...req.body, date: new Date().toLocaleDateString('vi-VN') };
  resources.unshift(newResource);
  await writeData(resources);
  res.status(201).json(newResource);
});

// PUT /api/resources/:id (update)
app.put('/api/resources/:id', async (req, res) => {
  const resources = await readData();
  const index = resources.findIndex(r => r.id === req.params.id);
  if (index !== -1) {
    resources[index] = { ...resources[index], ...req.body };
    await writeData(resources);
    res.json(resources[index]);
  } else {
    res.status(404).json({ error: 'Not found' });
  }
});

// DELETE /api/resources/:id
app.delete('/api/resources/:id', async (req, res) => {
  const resources = await readData();
  const filtered = resources.filter(r => r.id !== req.params.id);
  await writeData(filtered);
  res.status(204).send();
});

// Basic auth middleware for admin (simple header check)
app.use('/api/resources', (req, res, next) => {
  const auth = req.headers.authorization;
  if (auth === `Basic ${Buffer.from(ADMIN_PASS).toString('base64')}`) { // Expect 'Basic YWRtaW4xMjM='
    next();
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
});

app.listen(PORT, () => {
  console.log(`Server chạy tại http://localhost:${PORT}`);
  console.log(`Admin auth header: Basic ${Buffer.from(ADMIN_PASS).toString('base64')}`);
});
