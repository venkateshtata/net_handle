import { useState } from "react";
import AgentCard from "../components/agentCard.js";

const AgentStore = () => {

    const [searchTerm, setSearchTerm] = useState("");
    const cards = [
      { id: 1, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Health Assist", description: "Let me help you stay healthy", detailed_description: "Track fitness, diet, and overall wellness effectively." },
      { id: 2, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Budget Planner", description: "Spend less, save more", detailed_description: "Manage your expenses with personalized financial insights." },
      { id: 3, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Learning Companion", description: "Explore new topics with ease", detailed_description: "Access curated educational content and interactive learning tools." },
      { id: 4, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Accessibility Advocate", description: "Discover resources for differently-abled individuals", detailed_description: "Locate accessibility tools and inclusive community programs effortlessly." },
      { id: 5, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Mental Wellness Ally", description: "Support your journey to better mental health", detailed_description: "Access relaxation techniques and mental health support resources." },
      { id: 6, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Inclusive Educator", description: "Help bridge the gap in learning for everyone", detailed_description: "Provide tailored lessons and resources for diverse learning needs." },
      { id: 7, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Companion Connect", description: "Offer assistance and support for the underprivileged", detailed_description: "Facilitate connections to essential services and community aid." },
      { id: 8, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Event Organizer", description: "Make every occasion memorable", detailed_description: "Organize events seamlessly with automated reminders and planning tools." },
      { id: 9, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Creative Writer", description: "Boost your writing with creative ideas", detailed_description: "Generate story ideas and improve your writing with tips." },
      { id: 10, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Recipe Finder", description: "Find recipes with the ingredients you have", detailed_description: "Discover recipes based on your pantry ingredients." },
      { id: 11, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Book Recommender", description: "Discover your next favorite read", detailed_description: "Receive tailored book suggestions based on your interests." },
      { id: 12, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Daily Affirmations", description: "Start your day with positivity", detailed_description: "Boost motivation with daily inspirational affirmations." },
      { id: 13, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Home Organizer", description: "Organize your living space effectively", detailed_description: "Get tips and schedules to declutter and arrange your space." },
      { id: 14, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Tech Support", description: "Simplify troubleshooting for devices", detailed_description: "Get step-by-step solutions for technical issues." },
      { id: 15, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Idea Generator", description: "Fuel your brainstorming sessions", detailed_description: "Spark creativity with fresh and innovative suggestions." },
      { id: 16, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Gardening Helper", description: "Cultivate your green thumb", detailed_description: "Plan gardening activities with expert tips and seasonal guides." },
      { id: 17, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Stress Reliever", description: "Practice relaxation and mindfulness", detailed_description: "Learn mindfulness techniques to manage stress effectively." },
      { id: 18, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Code Assistant", description: "Write better code with smart tips", detailed_description: "Improve your programming with code snippets and debugging help." },
      { id: 19, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Art Mentor", description: "Inspire creativity and learn new techniques", detailed_description: "Access tutorials and ideas to enhance your artwork." },
      { id: 20, avatar: "https://www.shutterstock.com/image-vector/robot-icon-chatbot-cute-smiling-600nw-715418284.jpg", title: "Fitness Tracker", description: "Monitor and improve your activity", detailed_description: "Track exercise and set achievable fitness goals." }
    ];
  
    const filteredCards = cards.filter(card =>
      card.title.toLowerCase().includes(searchTerm.toLowerCase())
    );

  return (
    <div className="min-h-full text-white p-4 grid place-items-center items-start">
      <div className="sticky top-0 mb-6 h-40 w-full flex flex-col items-center">
        <div className="bg-white min-w-full text-center">
          <h1 className="text-4xl text-black font-silkscreen pt-4">Agent Hub</h1>
        </div>
        <div className="w-full grid place-items-center backdrop-blur-xl">
          <div className="w-full grid place-items-center  bg-gradient-to-t from-transparent to-white">
            <input
              type="text"
              className="mt-10 w-1/4 pl-6 py-2 rounded-full bg-black opacity-80 hover:shadow-2xl-dark text-white placeholder-gray-500 focus:outline-none transition duration:700"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-20">
        {filteredCards.map(card => (
          <div
            key={card.id}
          >
            <AgentCard avatar={card.avatar} title={card.title} description={card.description} detailed_description={card.detailed_description} />  
          </div>
        ))}
        {filteredCards.length === 0 && (
          <div className="col-span-full text-center text-gray-500">
            No results found.
          </div>
        )}
      </div>
    </div>
  )
}

export default AgentStore;