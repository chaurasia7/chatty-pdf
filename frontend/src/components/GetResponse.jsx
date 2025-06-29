import { useState, useRef, useEffect } from "react";

function GetResponse() {
  const [question, setQuestion] = useState("");   // Stores user input
  const [chat, setChat] = useState([]);           // Stores chat history
  const chatEndRef = useRef(null);                // Ref for auto-scrolling

  // Scrolls to bottom on every new message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  // Handles sending message and receiving response
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Update chat with user question
    const newChat = [...chat, { sender: "user", text: question }];
    setChat(newChat);
    setQuestion("");

    // Send question to backend
    const response = await fetch("http://127.0.0.1:8000/convo", {
      method: "POST",
      body: JSON.stringify({ question }),
      headers: { "Content-Type": "application/json" },
    });

    const data = await response.json();
    console.log(response);

    // Append bot's response to chat
    setChat([...newChat, { sender: "bot", text: data.answer }]);
  };

  return (
    <div className="flex flex-col justify-start w-full min-h-screen px-4 py-6 mt-8">
      {/* Chat History Display */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {chat.map((msg, index) => (
          <div key={index} className="flex items-start space-x-3">
            {/* Avatar */}
            <div className="flex-shrink-0">
              {msg.sender === "user" ? (
                <div className="w-8 h-8 bg-indigo-300 text-white font-semibold flex items-center justify-center rounded-full">
                  S
                </div>
              ) : (
                <div className="w-8 h-8 bg-green-100 flex items-center justify-center rounded-full">
                  <span className="text-green-700 font-bold text-sm">ai</span>
                </div>
              )}
            </div>

            {/* Chat Bubble */}
            <div
              className={`w-fit max-w-[85%] sm:max-w-[70%] md:max-w-[60%] lg:max-w-[50%] px-4 py-2 rounded-lg shadow ${
                msg.sender === "user"
                  ? "bg-green-100 text-gray-800"
                  : "bg-gray-200 text-gray-900"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      {/* Input Field */}
      <form
        onSubmit={handleSubmit}
        className="fixed bottom-0 left-0 w-full bg-white p-4 z-50"
      >
        <div className="relative w-full">
          <input
            type="text"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Send a message..."
            className="w-full bg-gray-100 border border-gray-300 rounded-sm px-4 pr-12 py-2 focus:outline-none"
            required
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 transform -translate-y-1/2 px-2 text-gray-400 hover:text-gray-500 text-lg"
          >
            ➤
          </button>
        </div>
      </form>
    </div>
  );
}

export default GetResponse;
