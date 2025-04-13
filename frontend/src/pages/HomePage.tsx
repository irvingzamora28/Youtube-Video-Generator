import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <Layout>
      <div className="bg-card shadow rounded-lg overflow-hidden">
        <div className="px-4 py-5 sm:p-6">
          <h1 className="text-2xl font-bold text-foreground mb-4">Welcome to StickEdu</h1>
          <p className="text-muted-foreground mb-4">
            Create educational videos with stickman figures and visual explanations.
          </p>
          <div className="mt-5 flex gap-3">
            <button
              type="button"
              onClick={() => navigate('/create')}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-primary-foreground bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              Create New Video
            </button>
            <button
              type="button"
              className="inline-flex items-center px-4 py-2 border border-border text-sm font-medium rounded-md text-foreground bg-card hover:bg-accent focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              Browse Examples
            </button>
          </div>
        </div>
      </div>

      <div className="mt-8 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Feature Card 1 */}
        <div className="bg-card shadow rounded-lg overflow-hidden border border-border">
          <div className="px-4 py-5 sm:p-6">
            <div className="text-primary mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-foreground">AI-Powered Content</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Generate educational content using advanced AI models like GPT and Gemini.
            </p>
          </div>
        </div>

        {/* Feature Card 2 */}
        <div className="bg-card shadow rounded-lg overflow-hidden border border-border">
          <div className="px-4 py-5 sm:p-6">
            <div className="text-primary mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-foreground">Stickman Animations</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Create engaging stickman animations to explain complex concepts visually.
            </p>
          </div>
        </div>

        {/* Feature Card 3 */}
        <div className="bg-card shadow rounded-lg overflow-hidden border border-border">
          <div className="px-4 py-5 sm:p-6">
            <div className="text-primary mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-foreground">Media Processing</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Combine text, images, and animations into professional-quality videos.
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
