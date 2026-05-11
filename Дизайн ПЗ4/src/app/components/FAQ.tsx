import { useState } from 'react';
import { ChevronDown } from 'lucide-react';

export function FAQ() {
  const [openQuestion, setOpenQuestion] = useState<number | null>(0);

  const faqs = [
    {
      question: 'Нужно ли уметь рисовать, чтобы стать моушн-дизайнером?',
      answer:
        'Нет, художественные навыки не обязательны. Моушн-дизайн — это работа с готовыми объектами, формами и типографикой. Главное — чувство композиции и ритма, которые мы развиваем на курсе.',
    },
    {
      question: 'Какой компьютер нужен для обучения?',
      answer:
        'Минимальные требования: процессор Intel i5 или аналог, 8 ГБ RAM, видеокарта с 2 ГБ памяти. Для комфортной работы рекомендуем 16 ГБ RAM. Подойдут как Windows, так и macOS.',
    },
    {
      question: 'Сколько времени нужно уделять учёбе?',
      answer:
        'Рекомендуем 10-15 часов в неделю: просмотр уроков (3-4 часа) и выполнение практических заданий (7-11 часов). График гибкий — можно учиться в удобное время.',
    },
    {
      question: 'Что если я не успею сдать проект вовремя?',
      answer:
        'Ничего страшного! Мы понимаем, что у всех разный темп. Доступ к материалам остаётся на 6 месяцев (навсегда в тарифе "С наставником"), так что вы сможете завершить всё в комфортном режиме.',
    },
    {
      question: 'Можно ли получить возврат, если курс не подойдёт?',
      answer:
        'Да, в течение первых 7 дней с момента старта курса мы вернём 100% оплаты без лишних вопросов, если вы поймёте, что обучение вам не подходит.',
    },
    {
      question: 'Помогаете ли с поиском работы после курса?',
      answer:
        'Да! Мы помогаем составить резюме, оформить портфолио на Behance, зарегистрироваться на биржах фриланса и консультируем по ценообразованию. У нас также есть закрытый чат выпускников для обмена опытом.',
    },
  ];

  return (
    <section id="faq" className="py-20 bg-gradient-to-b from-transparent via-purple-900/10 to-transparent">
      <div className="max-w-[1300px] mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Частые вопросы
          </h2>
          <p className="text-xl text-gray-400">
            Ответы на самые популярные вопросы о курсе
          </p>
        </div>

        <div className="space-y-4 max-w-3xl mx-auto">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className="bg-white/5 border border-white/10 rounded-xl overflow-hidden hover:border-purple-500/50 transition-colors"
            >
              <button
                onClick={() => setOpenQuestion(openQuestion === index ? null : index)}
                className="w-full p-6 flex items-center justify-between text-left hover:bg-white/5 transition-colors"
              >
                <span className="font-bold pr-4">{faq.question}</span>
                <ChevronDown
                  size={24}
                  className={`text-gray-400 flex-shrink-0 transition-transform ${
                    openQuestion === index ? 'rotate-180' : ''
                  }`}
                />
              </button>

              {openQuestion === index && (
                <div className="px-6 pb-6 border-t border-white/10">
                  <p className="text-gray-300 mt-4 leading-relaxed">{faq.answer}</p>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <p className="text-gray-400 mb-4">Не нашли ответ на свой вопрос?</p>
          <button className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-3 rounded-lg transition-all">
            Задать вопрос в чате
          </button>
        </div>
      </div>
    </section>
  );
}
