CREATE OR REPLACE VIEW public.mpa_polygon_category_view
AS SELECT m.mpa_id,
    m.geom,
    g.categories,
    m.wdpa_id,
    m.wdpa_pid,
    m.usmpa_id,
    m.name,
    m.orig_name,
    m.long_name,
    m.short_name,
    m.slug,
    m.country,
    m.sovereign,
    m.sub_location,
    m.designation,
    m.designation_eng,
    m.designation_type,
    m.iucn_category,
    m.int_criteria,
    m.marine,
    m.status,
    m.status_year,
    m.status_mpatlas,
    m.status_year_mpatlas,
    m.is_mpa,
    m.pa_def,
    m.implemented,
    m.implementation_date,
    m.no_take,
    m.no_take_area,
    m.no_take_mpatlas,
    m.no_take_area_mpatlas,
    m.no_take_wdpa,
    m.no_take_area_wdpa,
    m.rep_m_area,
    m.calc_m_area,
    m.calc_m_area_mpatlas,
    m.rep_area,
    m.calc_area,
    m.calc_area_mpatlas,
    m.gov_type,
    m.mgmt_auth,
    m.own_type,
    m.mgmt_plan_type,
    m.mgmt_plan_ref,
    m.glores_status,
    m.conservation_effectiveness,
    m.protection_level,
    m.fishing,
    m.fishing_info,
    m.fishing_citation,
    m.access,
    m.access_citation,
    m.primary_conservation_focus,
    m.secondary_conservation_focus,
    m.tertiary_conservation_focus,
    m.conservation_focus_citation,
    m.protection_focus,
    m.protection_focus_info,
    m.protection_focus_citation,
    m.constancy,
    m.constancy_citation,
    m.permanence,
    m.permanence_citation,
    m.wdpa_notes,
    m.notes,
    m.summary,
    m.is_point,
    m.verification_state,
    m.verified_date,
    m.other_ids,
    m.verification_reason,
    m.verified_by,
    m.verify_wdpa,
    m.conservation_focus_info,
    m.access_info
   FROM mpa_mpa m,
    ( SELECT n.mpa_id,
            string_agg(f.name::text, ', '::text ORDER BY (f.name::text)) AS categories
           FROM mpa_mpa n
             LEFT JOIN ( SELECT c.object_id,
                    a.name
                   FROM category_category a,
                    category_taggeditem c,
                    django_content_type d
                  WHERE a.id = c.tag_id AND d.app_label::text = 'mpa'::text AND d.model::text = 'mpa'::text AND c.content_type_id = d.id) f ON n.mpa_id = f.object_id
          GROUP BY n.mpa_id
          ORDER BY n.mpa_id) g
  WHERE m.geom IS NOT NULL AND m.is_point = false AND NOT m.verification_state::text = 'Rejected as MPA'::text AND m.mpa_id = g.mpa_id
  ORDER BY m.mpa_id DESC;

-- Rules and Triggers
CREATE OR REPLACE RULE mpa_polygon_category_view_INSERT as
    ON INSERT TO mpa_polygon_category_view DO INSTEAD
    INSERT INTO mpa_mpa 
    (geom,
    wdpa_id,
    wdpa_pid,
    usmpa_id,
    name,
    orig_name,
    long_name,
    short_name,
    slug,
    country,
    sovereign,
    sub_location,
    designation,
    designation_eng,
    designation_type,
    iucn_category,
    int_criteria,
    marine,
    status,
    status_year,
    status_mpatlas,
    status_year_mpatlas,
    is_mpa,
    pa_def,
    implemented,
    implementation_date,
    no_take,
    no_take_area,
    no_take_mpatlas,
    no_take_area_mpatlas,
    no_take_wdpa,
    no_take_area_wdpa,
    rep_m_area,
    calc_m_area,
    calc_m_area_mpatlas,
    rep_area,
    calc_area,
    calc_area_mpatlas,
    gov_type,
    mgmt_auth,
    own_type,
    mgmt_plan_type,
    mgmt_plan_ref,
    glores_status,
    conservation_effectiveness,
    protection_level,
    fishing,
    fishing_info,
    fishing_citation,
    access,
    access_citation,
    primary_conservation_focus,
    secondary_conservation_focus,
    tertiary_conservation_focus,
    conservation_focus_citation,
    protection_focus,
    protection_focus_info,
    protection_focus_citation,
    constancy,
    constancy_citation,
    permanence,
    permanence_citation,
    wdpa_notes,
    notes,
    summary,
    is_point,
    verification_state,
    verified_date,
    other_ids,
    verification_reason,
    verified_by,
    verify_wdpa,
    conservation_focus_info,
    access_info)
    VALUES
    (NEW.geom,
    NEW.wdpa_id,
    NEW.wdpa_pid,
    NEW.usmpa_id,
    NEW.name,
    NEW.orig_name,
    NEW.long_name,
    NEW.short_name,
    NEW.slug,
    NEW.country,
    NEW.sovereign,
    NEW.sub_location,
    NEW.designation,
    NEW.designation_eng,
    NEW.designation_type,
    NEW.iucn_category,
    NEW.int_criteria,
    NEW.marine,
    NEW.status,
    NEW.status_year,
    NEW.status_mpatlas,
    NEW.status_year_mpatlas,
    NEW.is_mpa,
    NEW.pa_def,
    NEW.implemented,
    NEW.implementation_date,
    NEW.no_take,
    NEW.no_take_area,
    NEW.no_take_mpatlas,
    NEW.no_take_area_mpatlas,
    NEW.no_take_wdpa,
    NEW.no_take_area_wdpa,
    NEW.rep_m_area,
    NEW.calc_m_area,
    NEW.calc_m_area_mpatlas,
    NEW.rep_area,
    NEW.calc_area,
    NEW.calc_area_mpatlas,
    NEW.gov_type,
    NEW.mgmt_auth,
    NEW.own_type,
    NEW.mgmt_plan_type,
    NEW.mgmt_plan_ref,
    NEW.glores_status,
    NEW.conservation_effectiveness,
    NEW.protection_level,
    NEW.fishing,
    NEW.fishing_info,
    NEW.fishing_citation,
    NEW.access,
    NEW.access_citation,
    NEW.primary_conservation_focus,
    NEW.secondary_conservation_focus,
    NEW.tertiary_conservation_focus,
    NEW.conservation_focus_citation,
    NEW.protection_focus,
    NEW.protection_focus_info,
    NEW.protection_focus_citation,
    NEW.constancy,
    NEW.constancy_citation,
    NEW.permanence,
    NEW.permanence_citation,
    NEW.wdpa_notes,
    NEW.notes,
    NEW.summary,
    NEW.is_point,
    NEW.verification_state,
    NEW.verified_date,
    NEW.other_ids,
    NEW.verification_reason,
    NEW.verified_by,
    NEW.verify_wdpa,
    NEW.conservation_focus_info,
    NEW.access_info);

CREATE OR REPLACE RULE mpa_polygon_category_view_UPDATE AS
    ON UPDATE TO mpa_polygon_category_view DO INSTEAD
    UPDATE mpa_mpa
    SET
        (mpa_id,
        geom,
        wdpa_id,
        wdpa_pid,
        usmpa_id,
        name,
        orig_name,
        long_name,
        short_name,
        slug,
        country,
        sovereign,
        sub_location,
        designation,
        designation_eng,
        designation_type,
        iucn_category,
        int_criteria,
        marine,
        status,
        status_year,
        status_mpatlas,
        status_year_mpatlas,
        is_mpa,
        pa_def,
        implemented,
        implementation_date,
        no_take,
        no_take_area,
        no_take_mpatlas,
        no_take_area_mpatlas,
        no_take_wdpa,
        no_take_area_wdpa,
        rep_m_area,
        calc_m_area,
        calc_m_area_mpatlas,
        rep_area,
        calc_area,
        calc_area_mpatlas,
        gov_type,
        mgmt_auth,
        own_type,
        mgmt_plan_type,
        mgmt_plan_ref,
        glores_status,
        conservation_effectiveness,
        protection_level,
        fishing,
        fishing_info,
        fishing_citation,
        access,
        access_citation,
        primary_conservation_focus,
        secondary_conservation_focus,
        tertiary_conservation_focus,
        conservation_focus_citation,
        protection_focus,
        protection_focus_info,
        protection_focus_citation,
        constancy,
        constancy_citation,
        permanence,
        permanence_citation,
        wdpa_notes,
        notes,
        summary,
        is_point,
        verification_state,
        verified_date,
        other_ids,
        verification_reason,
        verified_by,
        verify_wdpa,
        conservation_focus_info,
        access_info)
        =
        (NEW.mpa_id,
        NEW.geom,
        NEW.wdpa_id,
        NEW.wdpa_pid,
        NEW.usmpa_id,
        NEW.name,
        NEW.orig_name,
        NEW.long_name,
        NEW.short_name,
        NEW.slug,
        NEW.country,
        NEW.sovereign,
        NEW.sub_location,
        NEW.designation,
        NEW.designation_eng,
        NEW.designation_type,
        NEW.iucn_category,
        NEW.int_criteria,
        NEW.marine,
        NEW.status,
        NEW.status_year,
        NEW.status_mpatlas,
        NEW.status_year_mpatlas,
        NEW.is_mpa,
        NEW.pa_def,
        NEW.implemented,
        NEW.implementation_date,
        NEW.no_take,
        NEW.no_take_area,
        NEW.no_take_mpatlas,
        NEW.no_take_area_mpatlas,
        NEW.no_take_wdpa,
        NEW.no_take_area_wdpa,
        NEW.rep_m_area,
        NEW.calc_m_area,
        NEW.calc_m_area_mpatlas,
        NEW.rep_area,
        NEW.calc_area,
        NEW.calc_area_mpatlas,
        NEW.gov_type,
        NEW.mgmt_auth,
        NEW.own_type,
        NEW.mgmt_plan_type,
        NEW.mgmt_plan_ref,
        NEW.glores_status,
        NEW.conservation_effectiveness,
        NEW.protection_level,
        NEW.fishing,
        NEW.fishing_info,
        NEW.fishing_citation,
        NEW.access,
        NEW.access_citation,
        NEW.primary_conservation_focus,
        NEW.secondary_conservation_focus,
        NEW.tertiary_conservation_focus,
        NEW.conservation_focus_citation,
        NEW.protection_focus,
        NEW.protection_focus_info,
        NEW.protection_focus_citation,
        NEW.constancy,
        NEW.constancy_citation,
        NEW.permanence,
        NEW.permanence_citation,
        NEW.wdpa_notes,
        NEW.notes,
        NEW.summary,
        NEW.is_point,
        NEW.verification_state,
        NEW.verified_date,
        NEW.other_ids,
        NEW.verification_reason,
        NEW.verified_by,
        NEW.verify_wdpa,
        NEW.conservation_focus_info,
        NEW.access_info)
    WHERE mpa_id = NEW.mpa_id;

CREATE OR REPLACE RULE mpa_polygon_category_view_DELETE as
    ON DELETE TO mpa_polygon_category_view DO INSTEAD
     DELETE FROM mpa_mpa
     WHERE mpa_id=OLD.mpa_id;

-- Permissions

ALTER TABLE public.mpa_polygon_category_view OWNER TO mpatlas;
GRANT ALL ON TABLE public.mpa_polygon_category_view TO mpatlas;