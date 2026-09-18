import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_PATH = '/api/v1';

const api = axios.create({
  baseURL: `${API_BASE_URL}${API_PATH}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// E-book API
export const ebookApi = {
  create: (data: { title: string; author?: string; description?: string; format?: string }) =>
    api.post('/ebook/create', data),
  
  get: (id: number) =>
    api.get(`/ebook/${id}`),
  
  list: () =>
    api.get('/ebook/'),
  
  addResource: (id: number, resource: { type: string; source: string; title?: string; order?: number }) =>
    api.post(`/ebook/${id}/resources`, resource),
  
  uploadFile: (id: number, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/ebook/${id}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  generate: (id: number, data?: { chapters?: any[]; auto_extract?: boolean }) =>
    api.post(`/ebook/${id}/generate`, data || {}),
  
  getStatus: (id: number) =>
    api.get(`/ebook/${id}/status`),
  
  download: (id: number) =>
    api.get(`/ebook/${id}/download`, { responseType: 'blob' }),
  
  delete: (id: number) =>
    api.delete(`/ebook/${id}`),
};

// Templates API
export const templatesApi = {
  list: () =>
    api.get('/templates/'),
  
  get: (id: number) =>
    api.get(`/templates/${id}`),
  
  create: (data: { name: string; description?: string; category?: string; config?: any }) =>
    api.post('/templates/', data),
};

// Resources API
export const resourcesApi = {
  scrapeUrl: (url: string, usePlaywright: boolean = false) =>
    api.post('/resources/scrape', { url, use_playwright: usePlaywright }),
  
  searchImages: (query: string, count: number = 5) =>
    api.post('/resources/images/search', { query, count }),
  
  searchBooks: (query: string, maxResults: number = 10) =>
    api.post('/resources/books/search', { query, max_results: maxResults }),
  
  searchArchive: (query: string, mediaType: string = 'texts') =>
    api.post('/resources/archive/search', null, { params: { query, media_type: mediaType } }),
  
  summarizeContent: (text: string, maxLength: number = 130) =>
    api.post('/resources/content/summarize', null, { params: { text, max_length: maxLength } }),
};

export default api;
