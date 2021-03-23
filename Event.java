public class Event implements Comparable<Event>
{
    
    boolean entrance;
    double time;
    double elapsedTime;
    




    public Event(boolean entrance, double time, double elapsedTime) {
        this.entrance = entrance;
        this.time = time;
        this.elapsedTime = elapsedTime;
    }

    

    @Override
    public int compareTo(Event o) {
        if(o.getTime() > this.time)
            return -1;
        else if(o.getTime() < this.time)
            return 1;
        return 0;
    }





    public boolean isEntrance() {
        return entrance;
    }
    public void setEntrance(boolean entrance) {
        this.entrance = entrance;
    }
    public double getTime() {
        return time;
    }
    public void setTime(double time) {
        this.time = time;
    }

    public double getElapsedTime() {
        return elapsedTime;
    }


    public void setElapsedTime(double elapsedTime) {
        this.elapsedTime = elapsedTime;
    }


    
}
