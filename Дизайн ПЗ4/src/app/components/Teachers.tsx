import { Award, Briefcase } from 'lucide-react';

export function Teachers() {
  const teachers = [
    {
      name: 'Александр Соколов',
      position: 'Арт-директор в Яндекс',
      experience: '12 лет в индустрии',
      achievements: 'Работал над рекламными кампаниями для Samsung, Adidas, Red Bull',
      avatar: 'from-purple-600 to-purple-800',
    },
    {
      name: 'Мария Петрова',
      position: 'Lead Motion Designer в VK',
      experience: '8 лет в моушн-дизайне',
      achievements: 'Создала анимацию для топовых стриминговых платформ',
      avatar: 'from-pink-600 to-pink-800',
    },
    {
      name: 'Дмитрий Волков',
      position: 'Freelance Motion Designer',
      experience: '10 лет опыта',
      achievements: 'Более 200 завершённых проектов, топ-1% на Upwork',
      avatar: 'from-blue-600 to-blue-800',
    },
  ];

  return (
    <section id="teachers" className="py-20">
      <div className="max-w-[1300px] mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Преподаватели</h2>
          <p className="text-xl text-gray-400">
            Учитесь у практикующих специалистов из крупных компаний
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {teachers.map((teacher, index) => (
            <div
              key={index}
              className="bg-white/5 border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all group"
            >
              <div
                className={`w-24 h-24 bg-gradient-to-br ${teacher.avatar} rounded-full mx-auto mb-4 flex items-center justify-center text-3xl font-bold`}
              >
                {teacher.name.split(' ').map((n) => n[0]).join('')}
              </div>

              <h3 className="text-xl font-bold text-center mb-2">{teacher.name}</h3>
              <p className="text-purple-400 text-center mb-4">{teacher.position}</p>

              <div className="space-y-3">
                <div className="flex items-start gap-2">
                  <Briefcase size={20} className="text-gray-400 flex-shrink-0 mt-0.5" />
                  <span className="text-sm text-gray-300">{teacher.experience}</span>
                </div>
                <div className="flex items-start gap-2">
                  <Award size={20} className="text-gray-400 flex-shrink-0 mt-0.5" />
                  <span className="text-sm text-gray-300">{teacher.achievements}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
