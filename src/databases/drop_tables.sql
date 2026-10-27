begin;

drop schema if exists ingestion cascade;

drop table if exists
  public.travel,
  public.flight_state,
  public.weather_state,
  public.weather,
  public.icon,
  public.status,
  public.airport,
  public.timezone,
  public.aircraft,
  public.category,
  public.squawk,
  public.position_source,
  public.airline
cascade;

commit;