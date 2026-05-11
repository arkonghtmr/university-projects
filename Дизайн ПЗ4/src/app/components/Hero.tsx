import { Play, Sparkles } from 'lucide-react';

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center pt-[80px]">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-transparent to-pink-900/20" />

      <div className="max-w-[1300px] mx-auto px-4 py-20 relative z-10">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-6">
            <div className="inline-flex items-center gap-2 bg-purple-600/20 border border-purple-600/50 rounded-full px-4 py-2">
              <Sparkles size={16} className="text-purple-400" />
              <span className="text-sm text-purple-300">Старт потока 15 июня</span>
            </div>

            <h1 className="text-5xl md:text-6xl font-bold leading-tight">
              Моушн-дизайн{' '}
              <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                с нуля
              </span>
            </h1>

            <p className="text-xl text-gray-300 leading-relaxed">
              Освойте 2D и 3D анимацию за 2 месяца. Создайте портфолио из 5 работ
              и начните зарабатывать на творческих проектах
            </p>

            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <button className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-4 rounded-lg text-lg font-medium transition-all hover:scale-105 shadow-lg shadow-purple-600/50">
                Записаться на курс
              </button>
              <button className="border-2 border-white/20 hover:border-white/40 text-white px-8 py-4 rounded-lg text-lg font-medium transition-all">
                Бесплатная консультация
              </button>
            </div>

            {/* Stats */}
            <div className="flex gap-8 pt-6">
              <div>
                <div className="text-3xl font-bold text-purple-400">2 месяца</div>
                <div className="text-sm text-gray-400">Длительность</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-pink-400">5 проектов</div>
                <div className="text-sm text-gray-400">В портфолио</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-blue-400">100%</div>
                <div className="text-sm text-gray-400">Практики</div>
              </div>
            </div>
          </div>

          {/* Right - Video Showreel */}
          <div className="relative">
            <div className="aspect-video bg-gradient-to-br from-purple-900/50 to-pink-900/50 rounded-2xl border border-white/10 overflow-hidden relative group cursor-pointer">
              {/* Video placeholder with play button */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-20 h-20 bg-white/10 backdrop-blur-sm rounded-full flex items-center justify-center group-hover:bg-white/20 transition-all group-hover:scale-110">
                  <Play size={32} className="text-white ml-1" fill="white" />
                </div>
              </div>

              {/* Animated gradient overlay */}
              <div className="absolute inset-0 bg-gradient-to-tr from-purple-600/20 to-pink-600/20 animate-pulse" />

              {/* Mock video frames */}
              <div className="absolute top-4 left-4 right-4 flex gap-2">
                <div className="w-16 h-16 bg-purple-600/30 rounded" />
                <div className="w-16 h-16 bg-pink-600/30 rounded" />
                <div className="w-16 h-16 bg-blue-600/30 rounded" />
              </div>

              <div className="absolute bottom-4 right-4 bg-black/50 backdrop-blur-sm px-3 py-1 rounded-full text-xs">
                Шоурил студентов
              </div>
            </div>

            {/* Floating elements */}
            <div className="absolute -top-4 -right-4 w-24 h-24 bg-purple-600/20 rounded-full blur-2xl" />
            <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-pink-600/20 rounded-full blur-2xl" />
          </div>
        </div>
      </div>
    </section>
  );
}
