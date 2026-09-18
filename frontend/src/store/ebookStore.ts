import { create } from 'zustand';

export interface Ebook {
  id: number;
  title: string;
  author: string;
  status: string;
  format: string;
  created_at: string;
  description?: string;
  output_path?: string;
}

export interface Resource {
  id: number;
  type: string;
  source: string;
  title?: string;
  content?: string;
  order: number;
}

export interface Template {
  id: number;
  name: string;
  description?: string;
  category?: string;
  config?: any;
}

interface EbookStore {
  // State
  ebooks: Ebook[];
  currentEbook: Ebook | null;
  resources: Resource[];
  templates: Template[];
  loading: boolean;
  error: string | null;
  
  // Actions
  setEbooks: (ebooks: Ebook[]) => void;
  setCurrentEbook: (ebook: Ebook | null) => void;
  addEbook: (ebook: Ebook) => void;
  updateEbook: (id: number, updates: Partial<Ebook>) => void;
  removeEbook: (id: number) => void;
  
  setResources: (resources: Resource[]) => void;
  addResource: (resource: Resource) => void;
  
  setTemplates: (templates: Template[]) => void;
  
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useEbookStore = create<EbookStore>((set) => ({
  // Initial state
  ebooks: [],
  currentEbook: null,
  resources: [],
  templates: [],
  loading: false,
  error: null,
  
  // Actions
  setEbooks: (ebooks) => set({ ebooks }),
  
  setCurrentEbook: (ebook) => set({ currentEbook: ebook }),
  
  addEbook: (ebook) => set((state) => ({
    ebooks: [...state.ebooks, ebook],
  })),
  
  updateEbook: (id, updates) => set((state) => ({
    ebooks: state.ebooks.map((ebook) =>
      ebook.id === id ? { ...ebook, ...updates } : ebook
    ),
    currentEbook: state.currentEbook?.id === id
      ? { ...state.currentEbook, ...updates }
      : state.currentEbook,
  })),
  
  removeEbook: (id) => set((state) => ({
    ebooks: state.ebooks.filter((ebook) => ebook.id !== id),
    currentEbook: state.currentEbook?.id === id ? null : state.currentEbook,
  })),
  
  setResources: (resources) => set({ resources }),
  
  addResource: (resource) => set((state) => ({
    resources: [...state.resources, resource],
  })),
  
  setTemplates: (templates) => set({ templates }),
  
  setLoading: (loading) => set({ loading }),
  
  setError: (error) => set({ error }),
}));
