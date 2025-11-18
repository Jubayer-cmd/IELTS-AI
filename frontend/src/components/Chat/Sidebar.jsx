import { Card, CardContent } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Pin,
  Search,
  Plus,
  ChevronDown,
  Square,
  Settings,
  Sun,
  Menu,
  MessageSquarePlus,
  Trash2,
} from 'lucide-react';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { useState, useMemo } from 'react';

export default function Sidebar({
  threads = [],
  currentThreadId,
  onSelectThread,
  onNewThread,
  onDeleteThread,
  collapsed = false,
  onToggle
}) {
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [threadToDelete, setThreadToDelete] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const handleDeleteClick = (e, threadId) => {
    e.stopPropagation();
    setThreadToDelete(threadId);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (threadToDelete && onDeleteThread) {
      await onDeleteThread(threadToDelete);
      setDeleteDialogOpen(false);
      setThreadToDelete(null);
    }
  };

  // Filter threads based on search query with debouncing effect via useMemo
  const filteredThreads = useMemo(() => {
    if (!searchQuery.trim()) return threads;

    const query = searchQuery.toLowerCase();
    return threads.filter(thread =>
      (thread.title || 'New Chat').toLowerCase().includes(query)
    );
  }, [threads, searchQuery]);

  if (collapsed) {
    return (
      <div className='h-full bg-card border-r border-border flex flex-col items-center'>
        {/* Collapse Toggle */}
        <div className='p-3'>
          <button onClick={onToggle} className='p-2 hover:bg-accent rounded'>
            <Menu className='h-5 w-5 text-foreground' />
          </button>
        </div>

        {/* New Chat Button */}
        <div className='px-2 mb-4'>
          <Button
            onClick={onNewThread}
            className='w-10 h-10 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg flex items-center justify-center p-0'
          >
            <Plus className='h-4 w-4' />
          </Button>
        </div>

        {/* Search Icon */}
        <div className='px-2 mb-4'>
          <button className='w-10 h-10 hover:bg-accent rounded flex items-center justify-center'>
            <Search className='h-4 w-4 text-muted-foreground' />
          </button>
        </div>

        {/* Chat Icons */}
        <ScrollArea className='flex-1 px-2'>
          <div className='space-y-2'>
            {threads.slice(0, 3).map((thread) => (
              <div
                key={thread.id}
                onClick={() => onSelectThread(thread.id)}
                className={`w-10 h-8 rounded cursor-pointer ${currentThreadId === thread.id ? 'bg-accent' : 'bg-background hover:bg-accent'
                  }`}
              />
            ))}
          </div>
        </ScrollArea>

        {/* User Avatar */}
        <div className='p-3 border-t border-border'>
          <Avatar className='h-8 w-8 bg-muted'>
            <AvatarFallback className='text-muted-foreground text-sm'>
              J
            </AvatarFallback>
          </Avatar>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className='h-full bg-card border-r border-border flex flex-col'>
        {/* Header */}
        <div className='flex items-center justify-between px-4 py-4'>
          <div className='flex items-center gap-2 text-foreground font-semibold text-lg'>
            <button onClick={onToggle} className='p-1 hover:bg-accent rounded'>
              <Menu className='h-4 w-4 text-muted-foreground' />
            </button>
            IELTSAI
          </div>
          <div className='flex items-center gap-2'>
            <button className='p-1 hover:bg-accent rounded'>
              <Settings className='h-4 w-4 text-muted-foreground' />
            </button>
            <button className='p-1 hover:bg-accent rounded'>
              <Sun className='h-4 w-4 text-muted-foreground' />
            </button>
          </div>
        </div>

        {/* New Chat Button */}
        <div className='px-3 mb-4'>
          <Button
            onClick={onNewThread}
            className='w-full bg-primary hover:bg-primary/90 text-primary-foreground h-11 rounded-lg font-medium flex items-center justify-center gap-2'
          >
            <MessageSquarePlus className='h-4 w-4' />
            New Chat
          </Button>
        </div>

        {/* Search */}
        <div className='px-3 mb-4 relative'>
          <Input
            placeholder='Search your threads...'
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className='bg-input border-border text-foreground placeholder-muted-foreground pl-9 focus-visible:ring-primary'
          />
          <Search className='h-4 w-4 absolute left-6 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none' />
        </div>

        {/* Chat List */}
        <ScrollArea className='flex-1 px-3'>
          {filteredThreads.length === 0 ? (
            <div className='text-center text-muted-foreground text-sm py-8'>
              {searchQuery ? 'No threads found' : 'No threads yet. Start a new chat!'}
            </div>
          ) : (
            <div className='space-y-1'>
              {filteredThreads.map((thread) => (
                <div
                  key={thread.id}
                  onClick={() => onSelectThread(thread.id)}
                  className={`group px-3 py-2 rounded-lg cursor-pointer text-sm transition-colors flex items-center justify-between ${currentThreadId === thread.id
                      ? 'bg-accent text-foreground font-medium'
                      : 'text-foreground hover:bg-accent'
                    }`}
                >
                  <span className='truncate flex-1'>{thread.title || 'New Chat'}</span>
                  <button
                    type='button'
                    onClick={(e) => handleDeleteClick(e, thread.id)}
                    className='opacity-0 group-hover:opacity-100 p-1 hover:bg-destructive/10 rounded transition-opacity flex-shrink-0'
                  >
                    <Trash2 className='h-3.5 w-3.5 text-destructive' />
                  </button>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>

        {/* User Profile */}
        <div className='px-3 py-4 border-t border-border'>
          <div className='flex items-center gap-3'>
            <Avatar className='h-8 w-8 bg-muted'>
              <AvatarFallback className='text-muted-foreground text-sm'>
                J
              </AvatarFallback>
            </Avatar>
            <div>
              <div className='text-foreground text-sm font-medium'>Jubayer</div>
              <div className='text-muted-foreground text-xs'>Free</div>
            </div>
          </div>
        </div>
      </div>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Thread</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete this thread? This action cannot be undone and all messages will be permanently deleted.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button type='button' variant='outline' onClick={() => setDeleteDialogOpen(false)}>
              Cancel
            </Button>
            <Button type='button' variant='destructive' onClick={confirmDelete}>
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
