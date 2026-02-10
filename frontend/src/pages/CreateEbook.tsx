import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Save, Loader2, BookOpen } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { FileUploader } from '../components/upload/FileUploader';
import { URLInput } from '../components/upload/URLInput';
import { ebookApi, templatesApi } from '../services/api';
import { useEbookStore } from '../store/ebookStore';

export const CreateEbook: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const ebookId = searchParams.get('id');
  
  const { currentEbook, setCurrentEbook, addEbook, templates, setTemplates } = useEbookStore();
  
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [description, setDescription] = useState('');
  const [format, setFormat] = useState('epub');
  const [templateId, setTemplateId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    loadTemplates();
    if (ebookId) {
      loadEbook(Number(ebookId));
    }
  }, [ebookId]);

  const loadTemplates = async () => {
    try {
      const response = await templatesApi.list();
      setTemplates(response.data);
    } catch (error) {
      console.error('Failed to load templates:', error);
    }
  };

  const loadEbook = async (id: number) => {
    try {
      const response = await ebookApi.get(id);
      const ebook = response.data;
      setCurrentEbook(ebook);
      setTitle(ebook.title);
      setAuthor(ebook.author);
      setDescription(ebook.description || '');
      setFormat(ebook.format);
    } catch (error) {
      console.error('Failed to load e-book:', error);
    }
  };

  const handleCreateOrUpdate = async () => {
    if (!title) {
      alert('Please enter a title');
      return;
    }

    setLoading(true);
    try {
      if (currentEbook) {
        // Update existing
        alert('Update functionality coming soon');
      } else {
        // Create new
        const response = await ebookApi.create({
          title,
          author: author || 'Unknown',
          description,
          format,
        });
        const newEbook = response.data;
        setCurrentEbook(newEbook);
        addEbook(newEbook);
        navigate(`/create?id=${newEbook.id}`, { replace: true });
      }
    } catch (error: any) {
      console.error('Failed to create e-book:', error);
      alert(error.response?.data?.detail || 'Failed to create e-book');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (files: File[]) => {
    if (!currentEbook) {
      alert('Please create an e-book first');
      return;
    }

    for (const file of files) {
      try {
        await ebookApi.uploadFile(currentEbook.id, file);
      } catch (error) {
        console.error('Failed to upload file:', error);
      }
    }
  };

  const handleUrlAdded = async (data: any) => {
    if (!currentEbook) {
      alert('Please create an e-book first');
      return;
    }

    try {
      await ebookApi.addResource(currentEbook.id, {
        type: 'url',
        source: data.url,
        title: data.title,
      });
      alert('URL content added successfully!');
    } catch (error) {
      console.error('Failed to add URL resource:', error);
    }
  };

  const handleGenerate = async () => {
    if (!currentEbook) {
      alert('Please create an e-book first');
      return;
    }

    setGenerating(true);
    try {
      const response = await ebookApi.generate(currentEbook.id, {
        auto_extract: true,
      });
      alert(`Generation started! Task ID: ${response.data.task_id}`);
      
      // Poll for status
      const checkStatus = setInterval(async () => {
        const status = await ebookApi.getStatus(currentEbook.id);
        if (status.data.status === 'SUCCESS') {
          clearInterval(checkStatus);
          setGenerating(false);
          alert('E-book generated successfully!');
          navigate('/dashboard');
        } else if (status.data.status === 'FAILURE') {
          clearInterval(checkStatus);
          setGenerating(false);
          alert('Generation failed!');
        }
      }, 3000);
    } catch (error: any) {
      console.error('Failed to generate e-book:', error);
      alert(error.response?.data?.detail || 'Failed to generate e-book');
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">
            {currentEbook ? 'Edit E-book' : 'Create New E-book'}
          </h1>
          <p className="text-gray-500 mt-1">
            {currentEbook
              ? 'Add content and generate your e-book'
              : 'Start by entering basic information'}
          </p>
        </div>
        <Button variant="outline" onClick={() => navigate('/dashboard')}>
          Back to Dashboard
        </Button>
      </div>

      {/* Basic Information */}
      <Card>
        <CardHeader>
          <CardTitle>Basic Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Title *</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="Enter e-book title"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Author</label>
              <input
                type="text"
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
                className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="Enter author name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Description</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                rows={3}
                placeholder="Enter a brief description"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Format</label>
                <select
                  value={format}
                  onChange={(e) => setFormat(e.target.value)}
                  className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="epub">EPUB</option>
                  <option value="pdf">PDF</option>
                  <option value="html">HTML</option>
                  <option value="mobi">MOBI</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Template</label>
                <select
                  value={templateId || ''}
                  onChange={(e) => setTemplateId(Number(e.target.value) || null)}
                  className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="">Default</option>
                  {templates.map((template) => (
                    <option key={template.id} value={template.id}>
                      {template.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            {!currentEbook && (
              <Button onClick={handleCreateOrUpdate} disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating...
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    Create E-book
                  </>
                )}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Content Sources */}
      {currentEbook && (
        <>
          <Card>
            <CardHeader>
              <CardTitle>Add Content from Files</CardTitle>
            </CardHeader>
            <CardContent>
              <FileUploader onFilesSelected={handleFileUpload} />
            </CardContent>
          </Card>

          <URLInput onUrlAdded={handleUrlAdded} />

          <div className="flex justify-end gap-4">
            <Button
              onClick={handleGenerate}
              disabled={generating}
              size="lg"
            >
              {generating ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <BookOpen className="mr-2 h-5 w-5" />
                  Generate E-book
                </>
              )}
            </Button>
          </div>
        </>
      )}
    </div>
  );
};
