import { flushSync, useState } from "react";
import { Dialog, Transition, TransitionChild, DialogTitle, DialogPanel } from "@headlessui/react";

const FleetChat = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");


  // UNCOMMENT WHEN API
  // async function postMessage (message) {
  //   const res = await fetch("https://localhost/fleet/messages", {
  //       method: "POST",
  //       headers: {
  //       "Content-Type": "application/json",
  //       },
  //           body: JSON.stringify({
  //             id: 1,
  //             message: message,
  //             timestamp: new Date.toLocaleString()
  //       })
  //   });
  //  return res;



  const tmp_res = {
    "status": "success",
    "timestamp": "2024-11-15T14:30:00Z",
    "body": [
        {
            "id": "1",
            "message": "Hey, how are you?",
        },
    ]
}

  const sendMessage = () => {
    if (message.trim()) {
      setMessages([...messages, { text: message, sender: "user" }]);
      setMessages([...messages, {text: tmp_res["body"][0]["message"], sender: "fleet"}]);
      // setMessages([...messages,  { text: message, sender: "user" }, {text: tmp_res["body"][0]["message"], sender: "fleet"}])
      // console.log(tmp_res["body"][0])
      console.log(messages);
      setMessage(""); // Reset input
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
        sendMessage(); // Trigger the same function as the button
    }
  }

  return (
    <>
      {/* Trigger Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 p-3 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700"
      >
        Open Chat
      </button>

      {/* Chat Window Modal */}
      <Transition show={isOpen} as="div">
        <Dialog
          onClose={() => setIsOpen(false)}
          className="fixed inset-0 z-50 flex items-end justify-center p-4"
        >
          <TransitionChild
            enter="transition ease-out duration-300"
            enterFrom="opacity-0 translate-y-4"
            enterTo="opacity-100 translate-y-0"
            leave="transition ease-in duration-200"
            leaveFrom="opacity-100 translate-y-0"
            leaveTo="opacity-0 translate-y-4"
          >
            <DialogPanel className="w-full max-w-md p-4 bg-white rounded-lg shadow-lg">
              <DialogTitle className="text-lg font-bold">Chat</DialogTitle>
              <div className="mt-2 h-60 overflow-y-auto border rounded-md p-2">
                {/* Messages */}
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`mb-2 ${
                      msg.sender === "user" ? "text-right" : "text-left"
                    }`}
                  >
                    <span
                      className={`inline-block px-4 py-2 rounded-lg ${
                        msg.sender === "user"
                          ? "bg-blue-100 text-blue-800"
                          : "bg-gray-200 text-gray-800"
                      }`}
                    >
                      {msg.text}
                    </span>
                  </div>
                ))}
              </div>

              {/* Input Field */}
              <div className="mt-4 flex items-center">
                <input
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={handleKeyPress}
                  className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Type a message..."
                />
                <button
                  onClick={sendMessage}
                  className="ml-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Send
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </Dialog>
      </Transition>
    </>
  );
}

export default FleetChat;