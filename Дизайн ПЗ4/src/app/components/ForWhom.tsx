import { UserCircle, Briefcase, Palette } from 'lucide-react';

export function ForWhom() {
  const audience = [
    {
      icon: UserCircle,
      title: 'Новички без опыта',
      description:
        'Вы хотите освоить творческую профессию с нуля и работать удаленно. Мы научим вас всему с самых основ.',
      color: 'purple',
    },
    {
      icon: Briefcase,
      title: 'Смена профессии',
      description:
        'Работаете в сфере с низкой оплатой и хотите перейти в IT. Моушн-дизайн — ваш шанс на новый карьерный путь.',
      color: 'pink',
    },
    {
      icon: Palette,
      title: 'Графические дизайнеры',
      description:
        'Уже занимаетесь дизайном и хотите расширить навыки в анимацию. Добавьте в портфолио востребованный скилл.',
      color: 'blue',
    },
  ];

  const colorClasses = {
    purple: 'from-purple-600/20 to-purple-600/5 border-purple-600/30',
    pink: 'from-pink-600/20 to-pink-600/5 border-pink-600/30',
    blue: 'from-blue-600/20 to-blue-600/5 border-blue-600/30',
  };

  const iconColors = {
    purple: 'text-purple-400',
    pink: 'text-pink-400',
    blue: 'text-blue-400',
  };

  return (
    <section id="for-whom" className="py-20 relative">
      <div className="max-w-[1300px] mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Для кого этот курс
          </h2>
          <p className="text-xl text-gray-400">
            Обучение подходит для всех, кто хочет освоить моушн-дизайн
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {audience.map((item) => (
            <div
              key={item.title}
              className={`bg-gradient-to-br ${
                colorClasses[item.color as keyof typeof colorClasses]
              } border rounded-2xl p-8 hover:scale-105 transition-transform duration-300`}
            >
              <item.icon
                size={48}
                className={`mb-6 ${
                  iconColors[item.color as keyof typeof iconColors]
                }`}
              />
              <h3 className="text-2xl font-bold mb-4">{item.title}</h3>
              <p className="text-gray-300 leading-relaxed">{item.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
