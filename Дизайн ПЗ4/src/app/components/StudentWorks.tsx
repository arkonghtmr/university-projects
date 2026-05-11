import { Play } from 'lucide-react';

export function StudentWorks() {
  const works = [
    { title: '3D Product Animation', author: 'Анна К.', color: 'from-purple-600 to-blue-600' },
    { title: 'Logo Reveal', author: 'Дмитрий М.', color: 'from-pink-600 to-orange-600' },
    { title: 'Kinetic Typography', author: 'Елена С.', color: 'from-blue-600 to-cyan-600' },
    { title: 'Character Animation', author: 'Михаил В.', color: 'from-green-600 to-teal-600' },
    { title: 'Motion Graphics Reel', author: 'Ольга П.', color: 'from-purple-600 to-pink-600' },
    { title: 'Infographic Video', author: 'Сергей Л.', color: 'from-orange-600 to-red-600' },
  ];

  return (
    <section id="works" className="py-20 bg-gradient-to-b from-transparent via-pink-900/10 to-transparent">
      <div className="max-w-[1300px] mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Работы студентов</h2>
          <p className="text-xl text-gray-400">
            Реальные проекты выпускников, созданные на курсе
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {works.map((work, index) => (
            <div
              key={index}
              className="group relative aspect-video bg-gradient-to-br from-white/5 to-white/10 rounded-xl border border-white/10 overflow-hidden cursor-pointer hover:scale-105 transition-transform"
            >
              <div className={`absolute inset-0 bg-gradient-to-br ${work.color} opacity-50`} />

              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-16 h-16 bg-black/30 backdrop-blur-sm rounded-full flex items-center justify-center group-hover:bg-black/50 transition-colors">
                  <Play size={24} className="text-white ml-1" fill="white" />
                </div>
              </div>

              <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
                <div className="font-bold">{work.title}</div>
                <div className="text-sm text-gray-300">{work.author}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
