import React, { useState } from 'react';
import { Plus, Loader2 } from 'lucide-react';
import { Card, CardContent } from '../ui/Card';
import { Button } from '../ui/Button';
import { resourcesApi } from '@/services/api';

interface URLInputProps {
  onUrlAdded: (data: any) => void;
}

export const URLInput: React.FC<URLInputProps> = ({ onUrlAdded }) => {
  const [url, setUrl] = useState('');
  const [usePlaywright, setUsePlaywright] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!url) {
      setError('Please enter a URL');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await resourcesApi.scrapeUrl(url, usePlaywright);
      onUrlAdded(response.data);
      setUrl('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to scrape URL');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardContent className="p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Add Content from URL
            </label>
            <div className="flex gap-2">
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com/article"
                className="flex-1 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                disabled={loading}
              />
              <Button type="submit" disabled={loading}>
                {loading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Plus className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="playwright"
              checked={usePlaywright}
              onChange={(e) => setUsePlaywright(e.target.checked)}
              className="mr-2"
            />
            <label htmlFor="playwright" className="text-sm text-gray-600">
              Use JavaScript rendering (slower, for dynamic content)
            </label>
          </div>

          {error && (
            <div className="p-3 bg-destructive/10 text-destructive rounded-md text-sm">
              {error}
            </div>
          )}
        </form>
      </CardContent>
    </Card>
  );
};
