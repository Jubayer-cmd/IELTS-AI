import ChatWindow from '@/components/Chat/ChatWindow'

export default function HomePage() {
  return (
    <div className='h-full bg-[#1a1a1a] flex flex-col'>
        <div className='h-full'>
          <ChatWindow />
      </div>
    </div>
  )
}