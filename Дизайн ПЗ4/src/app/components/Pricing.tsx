import { Check, Star } from 'lucide-react';

export function Pricing() {
  const plans = [
    {
      name: 'Стандарт',
      price: '29 900',
      popular: false,
      features: [
        'Доступ ко всем урокам курса',
        'Проверка домашних заданий',
        'Чат с однокурсниками',
        'Сертификат о прохождении',
        'Доступ к материалам 6 месяцев',
      ],
    },
    {
      name: 'С наставником',
      price: '49 900',
      popular: true,
      features: [
        'Всё из тарифа "Стандарт"',
        'Личный наставник на весь курс',
        'Еженедельные созвоны 1-на-1',
        'Детальный разбор каждой работы',
        'Помощь в создании портфолио',
        'Консультация по трудоустройству',
        'Доступ к материалам навсегда',
      ],
    },
  ];

  return (
    <section id="pricing" className="py-20 bg-gradient-to-b from-purple-900/10 to-transparent">
      <div className="max-w-[1300px] mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Тарифы</h2>
          <p className="text-xl text-gray-400">
            Выберите подходящий вариант обучения
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`relative rounded-2xl p-8 flex flex-col ${
                plan.popular
                  ? 'bg-gradient-to-br from-purple-600/20 to-pink-600/20 border-2 border-purple-500'
                  : 'bg-white/5 border border-white/10'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-purple-600 to-pink-600 px-4 py-1 rounded-full flex items-center gap-1">
                  <Star size={16} fill="white" />
                  <span className="text-sm font-bold">Популярный</span>
                </div>
              )}

              <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
              <div className="mb-6">
                <span className="text-5xl font-bold">{plan.price} ₽</span>
                <span className="text-gray-400 ml-2">за весь курс</span>
              </div>

              <ul className="space-y-3 mb-8 flex-grow">
                {plan.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-start gap-3">
                    <Check
                      size={20}
                      className={`flex-shrink-0 mt-0.5 ${
                        plan.popular ? 'text-purple-400' : 'text-gray-400'
                      }`}
                    />
                    <span className="text-gray-300">{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                className={`w-full py-4 rounded-lg font-medium transition-all ${
                  plan.popular
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg shadow-purple-600/50'
                    : 'bg-white/10 hover:bg-white/20 text-white border border-white/20'
                }`}
              >
                Записаться на курс
              </button>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <p className="text-gray-400 mb-4">
            Возможна оплата в рассрочку на 4 месяца без процентов
          </p>
          <button className="text-purple-400 hover:text-purple-300 underline">
            Получить бесплатную консультацию
          </button>
        </div>
      </div>
    </section>
  );
}
