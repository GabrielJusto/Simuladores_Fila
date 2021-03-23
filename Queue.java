import java.util.ArrayList;

public class Queue 
{
    

    private int occupied;
    private Integer capacity;
    private int[] serviceTime;
    private int servers;
    private int[] avgClientTime;
    private ArrayList<Double> states;
    private double lastIn;


    public Queue(int[] serviceTime, int[] avgClientTime, int servers, int seed)
    {
        this.serviceTime = serviceTime;
        this.avgClientTime = avgClientTime;
        this.servers = servers;
        this.states = new ArrayList<>(capacity + 1);
        for(int i=0;i<capacity + 1;i++)
            states.add(0.0);

        lastIn = 0;
        occupied = 0;
    }

    public Queue(int capacity, int[] serviceTime, int[] avgClientTime, int servers, int seed)
    {
        this.capacity = capacity;
        this.serviceTime = serviceTime;
        this.avgClientTime = avgClientTime;
        this.servers = servers;
        this.states = new ArrayList<>(capacity + 1);
        for(int i=0;i<capacity + 1 ;i++)
            states.add(0.0);

        lastIn = 0;
        occupied = 0;
    }
    public ArrayList<Event> entrance(Event event)
    {
        lastIn = event.getTime();
        double elapsedTime = 0;
        ArrayList<Event> events = new ArrayList<>();
        states.set(occupied, states.get(occupied) + event.getElapsedTime());
        if(occupied < capacity)
        {
            occupied ++;
            if(occupied == 1)
            {
                elapsedTime = random(serviceTime[0], serviceTime[1]);
                events.add(new Event(false, event.getTime()+elapsedTime, elapsedTime));
            }
                
            
        }
        elapsedTime = random(avgClientTime[0], avgClientTime[1]);
        events.add(new Event(true, event.getTime()+elapsedTime, elapsedTime));


        return events;
    }

    public Event exit(Event event)
    {
        occupied --;
        states.set(occupied, event.getTime() - lastIn);

        if(occupied >= servers)
        {
            double elapsedTime = random(serviceTime[0], serviceTime[1]);
            lastIn = event.getTime();
            return new Event(false, event.getTime() + elapsedTime, elapsedTime);
           
        }
        return null;
    }



    


    public ArrayList<Double> getStates()
    {
        return this.states;
    }

}
