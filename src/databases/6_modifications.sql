--- repair exhausted sequence, 
--- handle some mismatches in schema

begin;

alter table public.flight_state
    alter column vertical_rate type numeric(6,2);

insert into public.position_source (
    position_source_id,
    opensky_code,
    position_source_val
)
values
    (1, 0, 'ADS_B'),
    (2, 1, 'ASTERIX'),
    (3, 2, 'MLAT'),
    (4, 3, 'FLARM')
on conflict (opensky_code) do update
set position_source_val = excluded.position_source_val;

select setval(
    'public.position_source_position_source_id_seq',
    (
        select max(position_source_id)
        from public.position_source
    ),
    true
);

commit;