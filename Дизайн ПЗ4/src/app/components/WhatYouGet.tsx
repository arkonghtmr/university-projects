import { Award, Briefcase, Code, Users } from 'lucide-react';

export function WhatYouGet() {
  const benefits = [
    {
      icon: Briefcase,
      title: 'Готовое портфолио',
      description: 'Шоурил из 5 профессиональных анимационных работ для демонстрации заказчикам',
    },
    {
      icon: Code,
      title: 'Владение софтом',
      description: 'Полное освоение After Effects и Cinema 4D — главных инструментов моушн-дизайнера',
    },
    {
      icon: Award,
      title: 'Сертификат',
      description: 'Официальный документ о прохождении курса для вашего резюме',
    },
    {
      icon: Users,
      title: 'Помощь в поиске заказов',
      description: 'Консультации по созданию профиля на биржах и привлечению первых клиентов',
    },
  ];

  return (
    <section className="py-20 bg-gradient-to-b from-transparent via-purple-900/10 to-transparent">
      <div className="max-w-[1300px] mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Что вы получите</h2>
          <p className="text-xl text-gray-400">
            Конкретные результаты после прохождения курса
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {benefits.map((benefit, index) => (
            <div
              key={index}
              className="bg-white/5 border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all group"
            >
              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-14 h-14 bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                    <benefit.icon size={28} className="text-white" />
                  </div>
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">{benefit.title}</h3>
                  <p className="text-gray-400">{benefit.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
