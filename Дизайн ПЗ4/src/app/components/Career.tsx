import { FileText, Users, TrendingUp, Handshake } from 'lucide-react';

export function Career() {
  const steps = [
    {
      icon: FileText,
      title: 'Резюме и портфолио',
      description: 'Поможем составить продающее резюме и оформить ваши работы на Behance',
    },
    {
      icon: Users,
      title: 'Регистрация на биржах',
      description: 'Создадим профили на Upwork, Freelancer и русскоязычных платформах',
    },
    {
      icon: TrendingUp,
      title: 'Стратегия продвижения',
      description: 'Расскажем, как находить первых клиентов и правильно оценивать работу',
    },
    {
      icon: Handshake,
      title: 'Поддержка после курса',
      description: 'Консультации в закрытом чате выпускников и разбор сложных кейсов',
    },
  ];

  return (
    <section className="py-20">
      <div className="max-w-[1300px] mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Помощь в трудоустройстве
          </h2>
          <p className="text-xl text-gray-400">
            Мы не бросаем вас после окончания курса
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((step, index) => (
            <div
              key={index}
              className="bg-gradient-to-br from-purple-900/20 to-pink-900/20 border border-purple-600/30 rounded-xl p-6 text-center hover:scale-105 transition-transform"
            >
              <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <step.icon size={32} className="text-white" />
              </div>
              <h3 className="text-xl font-bold mb-3">{step.title}</h3>
              <p className="text-gray-400 text-sm">{step.description}</p>
            </div>
          ))}
        </div>

        <div className="mt-12 bg-white/5 border border-white/10 rounded-2xl p-8 text-center">
          <p className="text-xl mb-4">
            <span className="font-bold text-purple-400">87%</span> наших выпускников
            находят первых заказчиков в течение{' '}
            <span className="font-bold text-pink-400">2 месяцев</span> после курса
          </p>
          <p className="text-gray-400">
            Средний доход начинающего моушн-дизайнера — от 60 000 ₽/месяц
          </p>
        </div>
      </div>
    </section>
  );
}
