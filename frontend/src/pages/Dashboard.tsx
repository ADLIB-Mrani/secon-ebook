import React, { useEffect } from 'react';
import { BookOpen, FileText, Download, Trash2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { useEbookStore } from '../store/ebookStore';
import { ebookApi } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { format } from 'date-fns';

export const Dashboard: React.FC = () => {
  const { ebooks, setEbooks, removeEbook, setLoading } = useEbookStore();
  const navigate = useNavigate();

  useEffect(() => {
    loadEbooks();
  }, []);

  const loadEbooks = async () => {
    setLoading(true);
    try {
      const response = await ebookApi.list();
      setEbooks(response.data);
    } catch (error) {
      console.error('Failed to load e-books:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this e-book?')) return;
    
    try {
      await ebookApi.delete(id);
      removeEbook(id);
    } catch (error) {
      console.error('Failed to delete e-book:', error);
      alert('Failed to delete e-book');
    }
  };

  const handleDownload = async (ebook: any) => {
    try {
      const response = await ebookApi.download(ebook.id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${ebook.title}.${ebook.format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Failed to download:', error);
      alert('E-book not ready for download yet');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-600 bg-green-50';
      case 'processing':
        return 'text-blue-600 bg-blue-50';
      case 'failed':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">My E-books</h1>
          <p className="text-gray-500 mt-1">Manage your e-book projects</p>
        </div>
        <Button onClick={() => navigate('/create')}>
          <BookOpen className="mr-2 h-4 w-4" />
          Create New E-book
        </Button>
      </div>

      {ebooks.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <BookOpen className="mx-auto h-16 w-16 text-gray-300 mb-4" />
            <h3 className="text-lg font-medium mb-2">No e-books yet</h3>
            <p className="text-gray-500 mb-4">
              Get started by creating your first e-book
            </p>
            <Button onClick={() => navigate('/create')}>Create E-book</Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {ebooks.map((ebook) => (
            <Card key={ebook.id}>
              <CardHeader>
                <CardTitle className="flex items-start justify-between">
                  <span className="line-clamp-1">{ebook.title}</span>
                  <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(ebook.status)}`}>
                    {ebook.status}
                  </span>
                </CardTitle>
                <CardDescription>by {ebook.author}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center text-sm text-gray-500">
                    <FileText className="mr-2 h-4 w-4" />
                    Format: {ebook.format.toUpperCase()}
                  </div>
                  <div className="text-xs text-gray-400">
                    Created {format(new Date(ebook.created_at), 'MMM dd, yyyy')}
                  </div>
                  <div className="flex gap-2 pt-2">
                    {ebook.status === 'completed' && (
                      <Button
                        size="sm"
                        onClick={() => handleDownload(ebook)}
                        className="flex-1"
                      >
                        <Download className="mr-1 h-3 w-3" />
                        Download
                      </Button>
                    )}
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => navigate(`/create?id=${ebook.id}`)}
                      className="flex-1"
                    >
                      View
                    </Button>
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => handleDelete(ebook.id)}
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
