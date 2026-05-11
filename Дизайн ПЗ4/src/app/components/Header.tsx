import { Menu, X } from 'lucide-react';
import { useState } from 'react';

interface HeaderProps {
  onNavigate: (id: string) => void;
}

export function Header({ onNavigate }: HeaderProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { label: 'Для кого', id: 'for-whom' },
    { label: 'Программа', id: 'program' },
    { label: 'Работы', id: 'works' },
    { label: 'Преподаватели', id: 'teachers' },
    { label: 'Тарифы', id: 'pricing' },
    { label: 'FAQ', id: 'faq' },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0f]/95 backdrop-blur-sm border-b border-white/10">
      <div className="max-w-[1300px] mx-auto px-4 h-[80px] flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg flex items-center justify-center">
            <span className="font-bold text-white">PA</span>
          </div>
          <div>
            <div className="font-bold text-lg">PixelArt</div>
            <div className="text-xs text-gray-400">Школа моушн-дизайна</div>
          </div>
        </div>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className="text-sm text-gray-300 hover:text-white transition-colors"
            >
              {item.label}
            </button>
          ))}
        </nav>

        {/* Price & CTA */}
        <div className="hidden md:flex items-center gap-4">
          <div className="text-right">
            <div className="text-sm text-gray-400">от</div>
            <div className="text-xl font-bold">29 900 ₽</div>
          </div>
          <button
            onClick={() => onNavigate('pricing')}
            className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-6 py-3 rounded-lg transition-all"
          >
            Записаться
          </button>
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden text-white"
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#0a0a0f] border-t border-white/10">
          <nav className="flex flex-col p-4">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  onNavigate(item.id);
                  setMobileMenuOpen(false);
                }}
                className="text-left py-3 text-gray-300 hover:text-white transition-colors border-b border-white/5"
              >
                {item.label}
              </button>
            ))}
            <button
              onClick={() => {
                onNavigate('pricing');
                setMobileMenuOpen(false);
              }}
              className="mt-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg"
            >
              Записаться — от 29 900 ₽
            </button>
          </nav>
        </div>
      )}
    </header>
  );
}
