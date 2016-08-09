package ru.lagner.android.academ_weather;


public class CustomEvent {
    public final int Id;
    public final String Description;
    public final String Extra;
    public final Object Data;

    public CustomEvent(final int id, final String desc, final String extra, final Object data) {
        this.Id = id;
        this.Description = desc;
        this.Extra = extra;
        this.Data = data;
    }
}
