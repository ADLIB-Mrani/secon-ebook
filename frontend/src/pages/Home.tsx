import React from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, Zap, Globe, FileText } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card';

export const Home: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: FileText,
      title: 'Multiple Sources',
      description: 'Import content from URLs, files, or APIs',
    },
    {
      icon: Zap,
      title: 'Fast Generation',
      description: 'Generate e-books in seconds with async processing',
    },
    {
      icon: Globe,
      title: 'Web Scraping',
      description: 'Extract content from any website automatically',
    },
    {
      icon: BookOpen,
      title: 'Multiple Formats',
      description: 'Export to EPUB, PDF, HTML, and MOBI',
    },
  ];

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center py-12">
        <h1 className="text-5xl font-bold mb-4">
          Secon E-book Generator
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Create professional e-books automatically from multiple sources.
          Scrape websites, import files, and generate beautiful e-books in minutes.
        </p>
        <div className="flex gap-4 justify-center">
          <Button size="lg" onClick={() => navigate('/create')}>
            <BookOpen className="mr-2 h-5 w-5" />
            Create Your First E-book
          </Button>
          <Button size="lg" variant="outline" onClick={() => navigate('/dashboard')}>
            View Dashboard
          </Button>
        </div>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        {features.map((feature, index) => (
          <Card key={index}>
            <CardHeader>
              <feature.icon className="h-10 w-10 text-primary mb-2" />
              <CardTitle>{feature.title}</CardTitle>
              <CardDescription>{feature.description}</CardDescription>
            </CardHeader>
          </Card>
        ))}
      </div>

      {/* How It Works */}
      <div>
        <h2 className="text-3xl font-bold text-center mb-8">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <CardContent className="p-6">
              <div className="text-4xl font-bold text-primary mb-2">1</div>
              <h3 className="text-lg font-semibold mb-2">Add Content</h3>
              <p className="text-gray-600">
                Upload files, paste URLs, or connect to APIs to gather your content
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="text-4xl font-bold text-primary mb-2">2</div>
              <h3 className="text-lg font-semibold mb-2">Customize</h3>
              <p className="text-gray-600">
                Choose templates, formats, and customize the appearance of your e-book
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="text-4xl font-bold text-primary mb-2">3</div>
              <h3 className="text-lg font-semibold mb-2">Generate</h3>
              <p className="text-gray-600">
                Click generate and download your professionally formatted e-book
              </p>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* CTA */}
      <div className="bg-primary/5 rounded-lg p-12 text-center">
        <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
        <p className="text-lg text-gray-600 mb-6">
          Create your first e-book in minutes
        </p>
        <Button size="lg" onClick={() => navigate('/create')}>
          Start Creating Now
        </Button>
      </div>
    </div>
  );
};
