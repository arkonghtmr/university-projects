import { Mail, Phone, Instagram, Youtube, Facebook, MessageCircle } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-black/50 border-t border-white/10 py-12">
      <div className="max-w-[1300px] mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* Company Info */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg flex items-center justify-center">
                <span className="font-bold text-white">PA</span>
              </div>
              <div className="font-bold text-lg">PixelArt</div>
            </div>
            <p className="text-sm text-gray-400 mb-4">
              Онлайн-школа цифровых профессий. Обучаем востребованным навыкам в IT и digital.
            </p>
            <div className="flex gap-3">
              <a
                href="#"
                className="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors"
              >
                <Instagram size={20} />
              </a>
              <a
                href="#"
                className="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors"
              >
                <Youtube size={20} />
              </a>
              <a
                href="#"
                className="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors"
              >
                <Facebook size={20} />
              </a>
              <a
                href="#"
                className="w-10 h-10 bg-white/10 hover:bg-white/20 rounded-lg flex items-center justify-center transition-colors"
              >
                <MessageCircle size={20} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-bold mb-4">Курсы</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Моушн-дизайн
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  UX/UI дизайн
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  3D-моделирование
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Веб-разработка
                </a>
              </li>
            </ul>
          </div>

          {/* About */}
          <div>
            <h4 className="font-bold mb-4">О школе</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  О нас
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Преподаватели
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Отзывы
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Блог
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-bold mb-4">Контакты</h4>
            <ul className="space-y-3 text-sm text-gray-400">
              <li className="flex items-center gap-2">
                <Mail size={16} />
                <a href="mailto:info@pixelart.ru" className="hover:text-white transition-colors">
                  info@pixelart.ru
                </a>
              </li>
              <li className="flex items-center gap-2">
                <Phone size={16} />
                <a href="tel:+78001234567" className="hover:text-white transition-colors">
                  8 (800) 123-45-67
                </a>
              </li>
              <li className="flex items-center gap-2">
                <MessageCircle size={16} />
                <a href="#" className="hover:text-white transition-colors">
                  Онлайн-чат
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-gray-400">
          <div>© 2026 PixelArt. Все права защищены.</div>
          <div className="flex gap-6">
            <a href="#" className="hover:text-white transition-colors">
              Политика конфиденциальности
            </a>
            <a href="#" className="hover:text-white transition-colors">
              Публичная оферта
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
