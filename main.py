        # Показываем статус "печатает"
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Формируем запрос
        prompt = f"{SYSTEM_PROMPT}\n\nПользователь: {message.text}"
        response = model.generate_content(prompt)
        
        # Если ответ пустой
        if not response.text:
            bot.reply_to(message, "Магас задумался и не смог подобрать слов. Попробуй еще раз.")
            return

        bot.reply_to(message, response.text)
        
    except Exception as e:
        error_msg = str(e)
        print(f"Ошибка: {error_msg}")
        
        if "429" in error_msg:
            bot.reply_to(message, "Йиш, лимиты Google временно исчерпаны. Магасу нужно 5 минут на отдых.")
        elif "API_KEY_INVALID" in error_msg:
            bot.reply_to(message, "Ошибка: Кажется, API ключ указан неверно. Проверь секреты в GitHub.")
        else:
            bot.reply_to(message, f"Связь барахлит (Ошибка: {error_msg[:50]}...)")

# 6. Запуск
if __name__ == "__main__":
    # Очищаем старые соединения перед стартом
    bot.remove_webhook()
    time.sleep(1)
    
    # Запуск веб-сервера
    Thread(target=run_web).start()
    
    print("Магас (версия 8b) вышел на связь...")
    # Бесконечный цикл работы
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
