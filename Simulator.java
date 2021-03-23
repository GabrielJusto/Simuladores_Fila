import java.util.ArrayList;
import java.util.PriorityQueue;

public class Simulator
{
   
    private static int STOP = 10;
    private static int CONS = 4;
    private static int MULT = 561;
    private static int MOD = 15619;
    private static int ITER = 200;

    public Simulator(int capacity)
    {
        int[] service = {3,6};
        int[] client = {1,2};
        PriorityQueue<Event> schedule = new PriorityQueue<>();
        int count = 0;




        Queue teste2 = new Queue(capacity, service, client, 1, 321);
        schedule.add(new Event(true, 2.00, 2.00));

        for(int i=0; i<STOP; i++)
        {
            Event e = schedule.poll();
            System.out.println(e.entrance + ", " + e.getTime());
            try{
                if(e.entrance)
                    schedule.addAll(teste2.entrance(e));
                
                else
                    schedule.add(teste2.exit(e));
            }catch(NullPointerException enull){}

        }

        System.out.println(teste2.getStates());
    }



    private double random(double a, double b)
    {
        return (b-a)*random() + a;
    }

    private ArrayList<Integer> random(int quant, int seed)  
    {
        double rand = seed;
        for(int i=0; i<ITER; i++)
            rand = ((MULT*rand) + CONS) % MOD;
          
        rand /= MOD ;
        
    }


}

