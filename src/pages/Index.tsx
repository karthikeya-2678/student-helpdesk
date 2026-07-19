import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-slate-100 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            Student Help Desk
          </h1>
          <p className="text-slate-400 text-lg">
            Flask + SQLite Application Ready for Download
          </p>
        </div>

        <Card className="bg-slate-800/50 border-slate-700 mb-8">
          <CardHeader>
            <CardTitle className="text-xl text-slate-100 flex items-center gap-3">
              <span className="text-2xl">📁</span>
              Project Files Created
            </CardTitle>
          </CardHeader>
          <CardContent className="text-slate-300">
            <p className="mb-4">
              All Flask application files are in the <code className="bg-slate-700 px-2 py-1 rounded text-cyan-400">flask-student-helpdesk/</code> folder:
            </p>
            <ul className="space-y-2 font-mono text-sm">
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> app.py - Main Flask application
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> requirements.txt - Python dependencies
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> templates/ - HTML templates (12 files)
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> static/css/style.css - Stylesheet
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> static/js/main.js - JavaScript
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> README.md - Full documentation
              </li>
            </ul>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 border-slate-700 mb-8">
          <CardHeader>
            <CardTitle className="text-xl text-slate-100 flex items-center gap-3">
              <span className="text-2xl">🚀</span>
              How to Run
            </CardTitle>
          </CardHeader>
          <CardContent className="text-slate-300">
            <ol className="space-y-4">
              <li className="flex gap-4">
                <span className="bg-blue-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold shrink-0">1</span>
                <div>
                  <p className="font-semibold text-slate-100">Download the files</p>
                  <p className="text-sm text-slate-400">Copy the flask-student-helpdesk folder to your local machine</p>
                </div>
              </li>
              <li className="flex gap-4">
                <span className="bg-blue-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold shrink-0">2</span>
                <div>
                  <p className="font-semibold text-slate-100">Install dependencies</p>
                  <code className="block bg-slate-900 p-3 rounded mt-2 text-sm text-cyan-400">
                    pip install -r requirements.txt
                  </code>
                </div>
              </li>
              <li className="flex gap-4">
                <span className="bg-blue-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold shrink-0">3</span>
                <div>
                  <p className="font-semibold text-slate-100">Run the application</p>
                  <code className="block bg-slate-900 p-3 rounded mt-2 text-sm text-cyan-400">
                    python app.py
                  </code>
                </div>
              </li>
              <li className="flex gap-4">
                <span className="bg-blue-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold shrink-0">4</span>
                <div>
                  <p className="font-semibold text-slate-100">Open in browser</p>
                  <p className="text-sm text-slate-400">Navigate to <code className="text-cyan-400">http://127.0.0.1:5000</code></p>
                </div>
              </li>
            </ol>
          </CardContent>
        </Card>

        <Card className="bg-emerald-900/30 border-emerald-700 mb-8">
          <CardHeader>
            <CardTitle className="text-xl text-emerald-100 flex items-center gap-3">
              <span className="text-2xl">🔐</span>
              Default Login Credentials
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-slate-800/50 p-4 rounded-lg">
                <h3 className="font-semibold text-slate-100 mb-2">Student Login</h3>
                <p className="text-sm text-slate-400">
                  Enter any name + roll number to auto-register
                </p>
              </div>
              <div className="bg-slate-800/50 p-4 rounded-lg">
                <h3 className="font-semibold text-slate-100 mb-2">Admin Login</h3>
                <p className="text-sm text-slate-300">
                  College: <code className="text-cyan-400">ABC College</code><br/>
                  Password: <code className="text-cyan-400">admin123</code>
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-xl text-slate-100 flex items-center gap-3">
              <span className="text-2xl">✨</span>
              Features Included
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6 text-slate-300">
              <div>
                <h3 className="font-semibold text-slate-100 mb-2">Student Portal</h3>
                <ul className="space-y-1 text-sm">
                  <li>• Simple login (name + roll number)</li>
                  <li>• 5 complaint categories</li>
                  <li>• Submit and track complaints</li>
                  <li>• View assigned admin details</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-slate-100 mb-2">Admin Portal</h3>
                <ul className="space-y-1 text-sm">
                  <li>• Secure admin login</li>
                  <li>• Profile setup on first login</li>
                  <li>• Take responsibility for complaints</li>
                  <li>• Update status (Pending → Resolved)</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        <p className="text-center text-slate-500 mt-8 text-sm">
          This is a complete Flask application. Download and run it locally on your server.
        </p>
      </div>
    </div>
  );
};

export default Index;
