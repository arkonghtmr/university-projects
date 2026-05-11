import { useState } from 'react';
import { Header } from './components/Header';
import { Hero } from './components/Hero';
import { ForWhom } from './components/ForWhom';
import { WhatYouGet } from './components/WhatYouGet';
import { Program } from './components/Program';
import { StudentWorks } from './components/StudentWorks';
import { Teachers } from './components/Teachers';
import { Pricing } from './components/Pricing';
import { Career } from './components/Career';
import { FAQ } from './components/FAQ';
import { Footer } from './components/Footer';

export default function App() {
  const [showGrid, setShowGrid] = useState(false);

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="relative bg-[#0a0a0f] min-h-screen text-white">
      {/* Grid Overlay Toggle */}
      <button
        onClick={() => setShowGrid(!showGrid)}
        className="fixed top-4 right-4 z-50 bg-purple-600 text-white px-4 py-2 rounded shadow-lg hover:bg-purple-700 text-sm"
      >
        {showGrid ? 'Скрыть сетку' : 'Показать сетку'}
      </button>

      {/* 12-Column Grid Overlay */}
      {showGrid && (
        <div className="fixed inset-0 pointer-events-none z-40">
          <div className="max-w-[1920px] h-full mx-auto">
            <div className="max-w-[1300px] h-full mx-auto grid grid-cols-12 gap-[20px]">
              {Array.from({ length: 12 }).map((_, i) => (
                <div
                  key={i}
                  className="bg-purple-500/10 border border-purple-500/30 h-full"
                />
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <Header onNavigate={scrollToSection} />
      <Hero />
      <ForWhom />
      <WhatYouGet />
      <Program />
      <StudentWorks />
      <Teachers />
      <Pricing />
      <Career />
      <FAQ />
      <Footer />
    </div>
  );
}
